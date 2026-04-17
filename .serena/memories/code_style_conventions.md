# Code Style & Conventions

## HTML pages
- Each page is a self-contained `<dir>/index.html` file. No templating engine — headers/footers are duplicated across pages.
- Every page MUST include:
  - `<title>` (specific, SEO-targeted)
  - `<meta name="description">`
  - `<link rel="canonical" href="https://karman.com.sg/...">`
  - Open Graph tags (`og:title`, `og:description`, `og:url`, `og:image`, `og:type`)
  - Twitter Card tags
- Blog posts additionally include `application/ld+json` with Article + BreadcrumbList schema.
- Service pages include Service-type JSON-LD.
- Stylesheet references are relative: `../../styles.css` from a 2-deep page.

## CSS
- Single global `styles.css` used site-wide. Page-specific rules (`blog.css`, `tools.css`) are loaded on top where needed.
- No CSS preprocessor, no CSS-in-JS. Plain CSS.
- Class naming is descriptive (no strict BEM), mostly kebab-case.

## JavaScript
- Vanilla JS, no framework, no bundler, no TypeScript.
- Global behaviors (header scroll, mobile nav, dropdowns, contact form, animations) live in `script.js`.
- Tool logic is centralised in `tools.js` as a single `TOOLS` object with per-tool step definitions + scoring logic. Individual tool landing pages in `tools/<name>/index.html` hook into this shared engine.

## Serverless API (`api/*.js`)
- Node.js 20, CommonJS (`module.exports = async (req, res) => {...}`).
- No npm dependencies; use built-in `crypto` + `fetch`.
- Email delivery via Resend REST API (`https://api.resend.com/emails`), auth'd with `RESEND_API_KEY`.
- OTP flow: `send-otp.js` generates an HMAC-signed token, `verify-otp.js` validates it before `send-result.js` releases the PDF/result email.

## SEO
- Canonical domain: `karman.com.sg` (no www, no trailing slash — enforced by `vercel.json`).
- `sitemap.xml` must be kept in sync when adding/removing pages.
- Internal links should use clean paths (`/blog/foo`, not `/blog/foo/index.html`).

## Blog post authoring
1. Create `blog/<slug>/index.html` (use an existing post as a template)
2. Fill structured data, canonical, OG tags, meta description
3. Add a card entry in `blog/index.html`
4. Add a `<url>` entry in `sitemap.xml`
