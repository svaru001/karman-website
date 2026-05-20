# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## Project Overview

Karman is a **static HTML/CSS/JS website** for a Singapore corporate services firm (incorporation, VCC fund administration, corporate secretary, accounting, GST, nominee director). Deployed on **Vercel** with serverless API routes.

**No build step, bundler, or framework.** HTML files are served directly. Vercel handles routing via `vercel.json` (clean URLs, no trailing slashes).

**Live domain:** `karman.com.sg` (no www)  
**Deploy flow:** `git push origin main` → Vercel auto-deploys via GitHub. Never use `vercel` CLI to deploy.

---

## Directory Structure

```
karman/
├── index.html              # Homepage
├── styles.css              # Global styles — loaded by every page
├── script.js               # Global JS — loaded by every page
├── blog.css                # Blog-only styles — loaded only by blog posts
├── tools.css               # Tool widget styles — loaded by blog posts + tool pages
├── tools.js                # Tool engine (all wizards: recommender, calculator, etc.)
├── vercel.json             # Routing: cleanUrls, trailingSlash:false, cache headers
├── sitemap.xml             # Must be updated when pages are added/removed
├── robots.txt              # Points to sitemap
├── rag-sources.json        # Source data for the RAG/AI chat backend
│
├── api/                    # Vercel serverless functions (Node.js, CommonJS)
│   ├── contact.js          # Contact + onboarding form → Resend email
│   ├── send-otp.js         # Generate HMAC OTP token for tool result unlock
│   ├── verify-otp.js       # Verify OTP before releasing tool results
│   └── send-result.js      # Send PDF results to user + lead notify to admin
│
├── blog/                   # 83+ blog posts (each is a directory with index.html)
│   └── <slug>/index.html
│
├── services/               # Service pages
│   ├── company-incorporation/
│   ├── vcc-fund-administration/
│   ├── corporate-secretary/
│   ├── accounting/
│   ├── gst-registration/
│   └── nominee-director/
│
├── for/                    # Audience-specific landing pages
│   ├── index.html          # Landing page hub
│   ├── india/              # Indian founders
│   ├── uae/                # UAE founders
│   ├── uk/                 # UK founders
│   ├── us/                 # US founders
│   ├── family-office/      # Family offices
│   ├── ai-startups/
│   ├── crypto/
│   ├── ecommerce/
│   ├── fintech/
│   └── saas/
│
├── tools/                  # Individual tool landing pages (link into tools.js engine)
│   ├── index.html
│   ├── business-structure-recommender/
│   ├── cost-calculator/
│   ├── eligibility-checker/
│   ├── incorporation-timeline/
│   ├── document-checklist/
│   ├── company-name-checker/
│   ├── compliance-health-check/
│   ├── ep-compass-calculator/
│   ├── singapore-tax-calculator/
│   └── ssic-code-search/
│
├── onboarding/             # Multi-step client onboarding form
├── ask/                    # Full-page AI chat (5 free queries, OTP unlock)
├── chat/                   # Floating chat widget (chat.css + chat.js, standalone only)
├── about/
├── faq/
├── glossary/
├── pricing/
├── partnerships/
├── admin/                  # Internal admin panel
├── brand/                  # Brand assets + preview page
└── templates/              # Downloadable .docx templates
```

---

## CSS & JS Loading Per Page Type

This is critical — getting this wrong causes invisible bugs (styles not applied, JS not running).

| Page type | styles.css | blog.css | tools.css | script.js | Inline `<style>` |
|---|---|---|---|---|---|
| Homepage (`index.html`) | `styles.css` (relative) | — | — | `script.js` (relative) | No |
| Service pages | `../../styles.css` | — | — | `/script.js` (absolute) | No |
| Blog posts | `../../styles.css` (in inline `<style>` comment block) | `../../blog.css` | `../../tools.css` | `/script.js` | **Yes — ~1,400 lines** |
| `/for/` landing pages | `../styles.css` or inline | — | — | `/script.js` | Some have inline |
| Tool pages | `../../styles.css` | — | `../../tools.css` | `/script.js` | No |
| Homepage blog section | — | — | — | — | — |

**Critical gotcha — blog posts have inline CSS:** Every blog post `index.html` contains a `<style>` block of ~1,400 lines of CSS copied from `styles.css`. This inline CSS loads *before* `../../blog.css` and `../../tools.css` (which are `<link>` tags just before `</body>`). Rules in the inline `<style>` block will be overridden by `blog.css` and `tools.css` if they have equal specificity. Rules in `blog.css`/`tools.css` apply to ALL blog posts without touching individual files — prefer modifying `blog.css` over editing individual post HTML.

---

## Z-Index Layers

Respect this stack when adding new fixed/absolute elements:

| Layer | z-index | Element |
|---|---|---|
| Blog contact modal overlay | `3000` | `.contact-modal-overlay` (in `blog.css`) |
| Tool modal | `2000` | Tool wizard overlay (in `tools.css`) |
| Site header (`.header`) | `1000` | Fixed top nav |
| Mobile nav menu | `999` | `.nav__menu.open` (slides down from header) |
| **Safe zone for new floating elements** | **< 999** | Don't exceed 999 or you'll overlap the nav |

**Do not place any new fixed element at `bottom: 24px; right: 24px`** — that position is reserved (previously used by the chat widget at `/chat/`). When adding floating buttons, use `bottom: 24px; left: 24px` or offset to `bottom: 88px; right: 24px`.

---

## script.js — Section Map

`script.js` is loaded on every page. Sections that are page-conditional check for a specific DOM element before running.

| Section | Condition | What it does |
|---|---|---|
| `GA4 CTA CLICK TRACKING` | Always | Tracks clicks on get_started, contact_us, email, phone, tool, ask_ai CTAs |
| `HEADER SCROLL EFFECT` | Always | Adds `.scrolled` class to `.header` on scroll |
| `MOBILE NAV TOGGLE` | Always | Hamburger menu open/close + X animation |
| `DROPDOWN CLICK TOGGLE` | If `.has-dropdown` exists | Opens/closes nav service dropdown |
| `SCROLL REVEAL ANIMATIONS` | Always | IntersectionObserver for `.reveal` elements |
| `PRICING TABS` | If `.pricing-tab` exists | Switches between Pte Ltd / VCC pricing tabs |
| `FAQ ACCORDION` | If `.faq-question` exists | Opens/closes FAQ items |
| `SMOOTH SCROLL` | Always | Smooth scrolls `a[href^="#"]` links |
| `CONTACT FORM` | If `#contactForm` exists | Validates + submits to `/api/contact` |
| `ACTIVE NAV LINK HIGHLIGHT` | Always | Highlights current page's nav link |
| `STATS COUNTER ANIMATION` | If `.stat-number` exists | Animates number counters on scroll |
| `AUTO-TOC FOR BLOG POSTS` | If `.article-body` exists | Injects a Table of Contents before first `<h2>` |
| `BLOG MOBILE CONTACT CTA` | If `.article-body` exists | Injects "Talk to us" orange pill button into nav + bottom-sheet contact modal |

---

## Blog Post Structure

Each blog post is a self-contained `index.html` (~1,900–2,100 lines). Template structure:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <!-- GTM snippet -->
  <!-- <meta> tags: charset, viewport, title, description, canonical, OG, Twitter -->
  <!-- Google Fonts (Sora + Inter) -->
  <style>
    /* ~1,400 lines: full copy of styles.css + blog-specific overrides */
    /* This is intentional — avoids a render-blocking external CSS request */
  </style>
  <!-- ld+json: Article + BreadcrumbList + FAQPage + WebPage schemas -->
</head>
<body>
  <!-- <header> with full nav + dropdowns (same markup as index.html) -->

  <main class="article-page-layout">
    <section class="article-hero"> <!-- Dark blue header with title + meta --> </section>

    <div class="article-layout">  <!-- CSS Grid: 1fr + 320px sidebar -->
      <article class="article-body">
        <!-- Table of Contents injected here by script.js AUTO-TOC -->
        <!-- <h2>, <h3>, <p>, tables, callout blocks (.callout), etc. -->
      </article>

      <aside class="article-sidebar">
        <div class="sidebar-cta">  <!-- "Get started from S$699" card --> </div>
        <div class="sidebar-tools"> <!-- Links to relevant tools --> </div>
        <!-- Topical sidebar tools (auto-generated per post category) -->
      </aside>
    </div>

    <section class="article-related"> <!-- 3 related post cards --> </section>
  </main>

  <!-- <footer> (same markup as index.html) -->

  <!-- Just before </body>: -->
  <link rel="stylesheet" href="../../tools.css" />
  <link rel="stylesheet" href="../../blog.css" />
  <script src="https://unpkg.com/lucide@latest/dist/umd/lucide.min.js"></script>
  <script>lucide.createIcons();</script>
  <script src="/script.js"></script>
</body>
```

**Article layout on mobile:** At `max-width: 768px`, `article-layout` becomes single-column (`grid-template-columns: 1fr`) with `padding: 32px 16px 56px`. The `.article-sidebar` gets `position: static` and `order: 2` (renders after the article body). Do not change `order` on the sidebar — it caused empty white space below the footer in a previous attempt.

---

## Blog Mobile Contact CTA ("Talk to us" pill)

Injected by `script.js` on all pages with `.article-body`. This is **DOM-injected** — no individual blog post HTML needs to be modified.

- **Button:** `.nav__msg-btn` — orange pill, inserted left of the hamburger in the nav, visible only on mobile (`max-width: 768px`)
- **Modal:** `.contact-modal-overlay` — fixed bottom-sheet (z-index: 3000), CSS in `blog.css`
- **Form submit:** POSTs to `/api/contact` with `form_name: 'blog_cta'` and `page: window.location.pathname`
- **Styling:** All CSS for this feature lives in `blog.css` (`.nav__msg-btn`, `.contact-modal-overlay`, `.contact-modal`, etc.)

---

## Adding New Blog Posts

1. Create `blog/<slug>/index.html` — copy an existing recent post as template (e.g. `blog/singapore-tax-savings-indian-textile-exporters/index.html`)
2. Update in the new file:
   - `<title>`, `<meta name="description">`, `<link rel="canonical">`
   - All Open Graph (`og:`) and Twitter Card tags
   - `ld+json` schemas: `Article.headline`, `Article.description`, `Article.url`, `Article.datePublished`, `BreadcrumbList`, `FAQPage` (if FAQ section exists)
   - Article hero: `<h1>`, meta items (date, read time, category tag)
   - Article body content
   - Related posts section (3 cards pointing to genuinely related posts)
3. Add a `.blog-card.reveal` entry in `blog/index.html`
4. Add a `BlogPosting` entry to the ld+json schema array in `blog/index.html`
5. Add a `<url>` entry in `sitemap.xml`

---

## Adding New Pages (Non-Blog)

1. Create `<section>/index.html` following an existing service or landing page
2. Load stylesheets via relative paths: `../../styles.css` (adjust depth as needed)
3. Load script via absolute path: `/script.js`
4. Add SEO tags: title, description, canonical, OG, Twitter, ld+json
5. Add to `sitemap.xml`

---

## Conversion Touchpoints

Understanding the existing CTAs prevents duplicating or conflicting with them:

| Touchpoint | Where | Target | Notes |
|---|---|---|---|
| "Get started" (nav, hero) | All pages | `/onboarding` | Primary high-intent CTA |
| "Contact us" (nav) | All pages | `#contact` | Secondary CTA |
| "Talk to us" pill | Blog posts, mobile only | Opens `.contact-modal-overlay` | Injected by `script.js`, styled in `blog.css` |
| Sidebar CTA | Blog posts, desktop | `/onboarding` | "Get started from S$699" dark card |
| Service card links | Homepage | `#contact` | "Get in touch →" on each service |
| CTA banner | Homepage | `#contact` | "Book a free consultation" |
| Contact form | Homepage `#contact` | `/api/contact` | Full form: name, email, phone, service, message |
| Onboarding form | `/onboarding` | `/api/contact` (source: onboarding) | Multi-step wizard |

**Phone number:** `+65 8074 3630` (used in `tel:` links and schema markup — same as WhatsApp Business number)  
**Admin email:** `team@karman.com.sg`

---

## Serverless API — Key Details

All functions in `api/` are CommonJS (`require`, `module.exports`). They use the Resend API for email.

**`api/contact.js`** accepts:
- Generic enquiry: `{ name, email, phone, service, message }`
- Onboarding: `{ name, email, phone, service, source: 'onboarding', entityType, stage, country, company, vcc }`
- Blog CTA (from `.contact-modal-overlay`): `{ name, email, message, form_name: 'blog_cta', page }`

Leads are also saved to a KV store if `KV_REST_API_URL` + `KV_REST_API_TOKEN` env vars are set.

---

## SEO Conventions

- Canonical domain: `https://karman.com.sg` (no www, no trailing slash)
- Every page: `<title>`, `<meta name="description">`, `<link rel="canonical">`, OG tags, Twitter Card tags
- Blog posts: `Article` + `BreadcrumbList` + `FAQPage` + `WebPage` ld+json schemas
- Service pages: `Service` or `LocalBusiness` ld+json schema
- `sitemap.xml` — update `<lastmod>` and add `<url>` entries when pages change
- Blog post priorities in sitemap: `0.80` for pillar content, `0.70` for supporting posts

---

## Development

No install or build required.

```bash
# Full local dev (static + API routes):
npx vercel dev

# Static-only (no API):
python3 -m http.server 8000
```

Requires `vercel` CLI linked to the project for env vars when using `npx vercel dev`.

---

## Known Issues / Past Mistakes to Avoid

- **Do not change `order` on `.article-sidebar` in `blog.css`** — changing it from `order: 2` caused empty white space below the footer on mobile. The sidebar correctly renders after the article body on mobile.
- **Do not add floating fixed elements at `bottom: 24px; right: 24px`** — that position collides with potential future chat widget placement.
- **When adding site-wide JS features via `script.js`**, always guard with a DOM check (`if (!document.querySelector('.article-body')) return;`) if the feature is blog-only, to avoid running on every page.
- **Blog post inline CSS overrides matter** — if a `blog.css` rule isn't applying to a blog post, check if the inline `<style>` block has a higher-specificity rule for the same selector.
- **SVG icons in JS-injected elements** — test SVG rendering before deploying. Multi-path SVGs can render incorrectly depending on fill-rule and path ordering. Prefer single-path SVGs for injected icons.
