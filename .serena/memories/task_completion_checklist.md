# Task Completion Checklist

There is no automated test / lint / type-check pipeline. "Done" is verified manually.

## For any page change
- [ ] Canonical URL uses `https://karman.com.sg/<clean-path>` (no www, no trailing slash, no `.html`)
- [ ] `<title>`, meta description, OG tags, Twitter card tags present and correct
- [ ] Relative asset paths resolve from the page's directory depth
- [ ] Header nav + footer match other pages (duplicated across files — keep them in sync)
- [ ] Open the page locally in a browser and sanity-check layout on desktop + mobile widths

## When adding a new page (blog, service, tool, etc.)
- [ ] Add `<url>` entry to `sitemap.xml`
- [ ] Add a card/link on the relevant hub page (e.g. `blog/index.html`, `services/` landing)
- [ ] Structured data (`application/ld+json`) included where applicable (Article for blog, Service for services)

## When removing a page
- [ ] Remove from `sitemap.xml`
- [ ] Remove cards/links pointing to it
- [ ] Consider a redirect in `vercel.json` if the URL was indexed

## For API / backend changes
- [ ] `npx vercel dev` starts without errors
- [ ] Required env vars present locally (`npx vercel env pull` if missing)
- [ ] Manually trigger the endpoint (submit the form / click the button) and confirm the expected email arrives

## Before committing
- [ ] `git status` — review changed files
- [ ] `git diff` — scan for accidental edits
- [ ] No secrets, API keys, or personal emails hardcoded
- [ ] Commit message follows repo style (short imperative, e.g. `Add foo`, `Update bar`, `Fix baz`)

## After deploy (Vercel auto-deploys on push to `main`)
- [ ] Visit the live URL, confirm the change rendered
- [ ] For new pages: check Google Search Console / request re-index if time-sensitive
