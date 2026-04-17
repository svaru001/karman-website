# Suggested Commands (Darwin / macOS)

## Run locally
```bash
# Full stack (static + api/ serverless functions). Requires vercel CLI + linked project.
npx vercel dev

# Static only (no API routes)
python3 -m http.server 8000
```

## Deploy
```bash
# Preview
npx vercel

# Production
npx vercel --prod
```
Deployment is typically triggered by git push to `main` (linked Vercel project auto-deploys).

## Env vars (set in Vercel dashboard, NOT committed)
- `RESEND_API_KEY` — Resend email API key
- `ADMIN_EMAIL` — notification recipient, defaults to `team@karman.com.sg`
- `OTP_SECRET` — HMAC secret for OTP token signing

Pull env vars locally:
```bash
npx vercel env pull
```

## Git
```bash
git status
git diff
git log --oneline -20
```

## System utilities (Darwin)
- `ls`, `cd`, `pwd`, `cat`, `open` — macOS ships BSD variants; prefer the Grep/Glob/Read tools over raw `grep`/`find`/`cat` in this environment.
- `ripgrep` is available via the Grep tool.

## Testing / Linting / Formatting
**None configured.** No test suite, no linter, no formatter, no CI beyond Vercel's build step (which for a static site is effectively a no-op). Validation is manual:
- Open changed pages in browser, verify layout + forms + tools flow
- Check canonical URLs, OG tags, structured data (JSON-LD) by view-source
- If you add a page: update `sitemap.xml` and add a card/link on the relevant hub page

## When a task is considered "complete"
See `task_completion_checklist.md`.
