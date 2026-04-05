/* ─────────────────────────────────────────────
   KARMAN — Verify OTP (stateless, HMAC-based)
   POST /api/verify-otp
   Accepts { token, otp, email }
   Returns  { ok: true } or 4xx error
───────────────────────────────────────────── */

const crypto = require('crypto');

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).end();

  const { token, otp, email } = req.body;

  if (!token || !otp || !email) {
    return res.status(400).json({ error: 'Missing required fields' });
  }

  let decoded;
  try {
    decoded = Buffer.from(token, 'base64').toString();
  } catch (_) {
    return res.status(400).json({ error: 'Invalid token' });
  }

  // token format: email:otp:expiry:hmac
  // Split from right: last segment is hmac, then expiry, then otp, then email (which may contain @)
  const parts = decoded.split(':');
  if (parts.length < 4) return res.status(400).json({ error: 'Malformed token' });

  const providedHmac = parts[parts.length - 1];
  const expiry       = parseInt(parts[parts.length - 2]);
  const tokenOtp     = parts[parts.length - 3];
  const tokenEmail   = parts.slice(0, parts.length - 3).join(':');
  const payload      = parts.slice(0, parts.length - 1).join(':');

  // Validate HMAC
  const secret       = process.env.RESEND_API_KEY || 'dev-secret-change-me';
  const expectedHmac = crypto.createHmac('sha256', secret).update(payload).digest('hex');

  let hmacMatch = false;
  try {
    hmacMatch = crypto.timingSafeEqual(
      Buffer.from(providedHmac, 'hex'),
      Buffer.from(expectedHmac, 'hex'),
    );
  } catch (_) {
    return res.status(401).json({ error: 'Invalid token' });
  }

  if (!hmacMatch) return res.status(401).json({ error: 'Invalid token' });

  if (Date.now() > expiry) {
    return res.status(401).json({ error: 'Code has expired. Please request a new one.' });
  }

  if (tokenEmail.toLowerCase() !== email.toLowerCase()) {
    return res.status(401).json({ error: 'Email mismatch' });
  }

  if (tokenOtp !== otp.trim()) {
    return res.status(401).json({ error: 'Incorrect code — please try again.' });
  }

  return res.status(200).json({ ok: true });
};
