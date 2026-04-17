# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Karman is a **static HTML/CSS/JS website** for a Singapore corporate services firm (incorporation, VCC fund administration, corporate secretary, accounting, GST, nominee director). It is deployed on **Vercel** with serverless API routes.

There is no build step, bundler, or framework. HTML files are served directly. Vercel handles routing via `vercel.json` (clean URLs, no trailing slashes).

## Architecture

### Frontend (static, no build)
- **`index.html`** — Homepage (single large file with all sections)
- **`styles.css`** — Global styles (used by all pages)
- **`script.js`** — Global JS: header scroll, mobile nav, dropdowns, contact form, animations
- **`tools.css` / `tools.js`** — Interactive tool engine: multi-step wizards (business structure recommender, cost calculator, eligibility checker, incorporation timeline, document checklist). All tool logic lives in `tools.js` as a single `TOOLS` object with step definitions and scoring logic
- **`blog.css`** — Blog article styling

### Page structure
Every subpage lives in its own directory as `index.html` (e.g., `services/company-incorporation/index.html`, `blog/variable-capital-company-singapore-vcc/index.html`). Pages reference root stylesheets via relative paths (`../../styles.css`).

### Serverless API (`api/`)
All endpoints are Vercel serverless functions (Node.js, CommonJS). They use the **Resend** email API.

| Endpoint | Purpose |
|---|---|
| `api/contact.js` | Contact form + onboarding form submissions → email to admin |
| `api/send-otp.js` | Email OTP for tool results (generates HMAC token) |
| `api/verify-otp.js` | Verifies OTP token before releasing tool results |
| `api/send-result.js` | Sends PDF results to user + lead notification to admin |

**Environment variables** (set in Vercel dashboard):
- `RESEND_API_KEY` — Resend email API key
- `ADMIN_EMAIL` — Notification recipient (defaults to team@karman.com.sg)
- `OTP_SECRET` — HMAC secret for OTP token signing

### AI Chat
- **`chat/`** — Floating chat widget (compliance assistant)
- **`ask/`** — Full-page AI chat with query limits (5 free, then OTP unlock)
- Both hit a RAG backend at `https://karman-rag-production.up.railway.app` (hosted on Railway, separate repo)
- **`rag-sources.json`** — Source data for the RAG system

### Other directories
- **`onboarding/`** — Multi-step client onboarding flow
- **`brand/`** — Brand assets and preview page
- **`tools/`** — Individual tool landing pages (each links into the shared `tools.js` engine)

## Development

No install or build required. To develop locally:

```bash
npx vercel dev
```

This serves the static site and runs the `api/` serverless functions locally. Requires `vercel` CLI and linked project for env vars.

For static-only preview (no API routes), any local server works:
```bash
python3 -m http.server 8000
```

## SEO Conventions

- Every page has: `<title>`, `<meta name="description">`, `<link rel="canonical">`, Open Graph tags, Twitter Card tags
- Blog posts include `application/ld+json` structured data (Article + BreadcrumbList schema)
- Service pages include `ld+json` structured data
- `sitemap.xml` must be kept in sync when adding/removing pages
- `robots.txt` points to the sitemap
- Canonical domain is `karman.com.sg` (no www)

## Blog Post Pattern

To add a new blog post:
1. Create `blog/<slug>/index.html` following an existing post as template
2. Include structured data (`ld+json`), canonical URL, OG tags, meta description
3. Add a card entry in `blog/index.html` (the blog hub page)
4. Add a `<url>` entry in `sitemap.xml`
