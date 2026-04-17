# Serverless API Endpoints

All live in `api/`, Node 20 CommonJS, zero npm deps. All use Resend for email.

| File | Route | Purpose |
|---|---|---|
| `api/contact.js` | `POST /api/contact` | Contact form + onboarding form submissions. Sends notification email to `ADMIN_EMAIL`. |
| `api/send-otp.js` | `POST /api/send-otp` | Generates a 6-digit OTP, signs an HMAC token with `OTP_SECRET`, emails the OTP to the user. Returns the signed token to the client. |
| `api/verify-otp.js` | `POST /api/verify-otp` | Verifies submitted OTP against the signed token. Gates access to tool results and the `ask/` chat beyond the free-query limit. |
| `api/send-result.js` | `POST /api/send-result` | After OTP verified, sends the PDF/tool result to the user and a lead-notification email to `ADMIN_EMAIL`. |

## Required env vars (Vercel dashboard)
- `RESEND_API_KEY`
- `ADMIN_EMAIL` (defaults to `team@karman.com.sg`)
- `OTP_SECRET`

## Consumers
- `script.js` → `/api/contact` (homepage + service page contact forms)
- `onboarding/` flow → `/api/contact`
- `tools.js` → `/api/send-otp` → `/api/verify-otp` → `/api/send-result`
- `ask/` page → same OTP chain as tools, once free queries exhausted
- `chat/` widget → external RAG backend at `karman-rag-production.up.railway.app` (NOT an `api/` route)
