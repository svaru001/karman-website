# Karman — Project Overview

## Purpose
Marketing + lead-gen website for **Karman**, a Singapore corporate services firm. Services covered: company incorporation, VCC fund administration, corporate secretary, accounting, GST registration, nominee director.

Primary audiences: foreign founders (US, UK, India, China/HK, Indonesia, Australia, Gulf) considering Singapore incorporation; fund managers considering VCC / re-domiciliation from Cayman / DIFC / ADGM.

## Tech Stack
- **Static HTML/CSS/JS** — no build step, no bundler, no framework.
- **Hosting:** Vercel. Clean URLs, no trailing slashes (see `vercel.json`).
- **Serverless API:** Node.js 20 CommonJS functions in `api/`.
- **Email:** Resend API (used by all API routes).
- **RAG backend:** separate repo at `https://karman-rag-production.up.railway.app` (Railway). Consumed by `chat/` widget and `ask/` full page.
- **Node:** `engines.node = "20.x"` in `package.json`. No dependencies declared — APIs use fetch + crypto only, no npm install needed.

## High-Level Layout
- `index.html` — homepage (single large file, all sections inlined)
- `styles.css` / `script.js` — global site styles + nav/form/animation JS
- `tools.css` / `tools.js` — shared multi-step wizard engine used by all tools
- `blog.css` — blog article styles
- Pages live as `<dir>/index.html` (e.g. `services/company-incorporation/index.html`)
- Assets referenced via relative paths (`../../styles.css`)

## Directories
- `api/` — 4 serverless functions (contact, send-otp, verify-otp, send-result)
- `services/` — 6 service pages (company-incorporation, vcc-fund-administration, corporate-secretary, accounting, gst-registration, nominee-director)
- `tools/` — 5 interactive tools + hub index (business-structure-recommender, cost-calculator, document-checklist, eligibility-checker, incorporation-timeline)
- `blog/` — 37 blog posts + hub index (`blog/index.html`)
- `chat/` — floating compliance chat widget (RAG)
- `ask/` — full-page AI chat with OTP-gated query limit (5 free queries)
- `onboarding/` — multi-step client onboarding flow
- `brand/` — brand assets + preview page
- `about/`, `pricing/`, `faq/` — static info pages
- `rag-sources.json` — source data consumed by the RAG backend
- `sitemap.xml`, `robots.txt`, `favicon.*`, `logo.*` — site root assets

## Canonical Domain
`karman.com.sg` (no www). All canonical tags + OG URLs must use this.
