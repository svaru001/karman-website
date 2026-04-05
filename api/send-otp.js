/* ─────────────────────────────────────────────
   KARMAN — Send OTP via Resend (email)
   POST /api/send-otp
   Body: { email }
   Returns: { token }
───────────────────────────────────────────── */

const crypto = require('crypto');

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).end();

  const { email } = req.body;
  if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    return res.status(400).json({ error: 'Valid email address required' });
  }

  const key = process.env.RESEND_API_KEY;
  if (!key) return res.status(500).json({ error: 'Email service not configured' });

  // Generate 6-digit OTP
  const otp    = String(Math.floor(100000 + Math.random() * 900000));
  const expiry = Date.now() + 10 * 60 * 1000; // 10 minutes

  // Signed token: base64(email:otp:expiry:hmac)
  const payload = `${email}:${otp}:${expiry}`;
  const hmac    = crypto.createHmac('sha256', key).update(payload).digest('hex');
  const token   = Buffer.from(`${payload}:${hmac}`).toString('base64');

  // Send OTP email via Resend
  const emailRes = await fetch('https://api.resend.com/emails', {
    method:  'POST',
    headers: { 'Authorization': `Bearer ${key}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({
      from:    'Karman <onboarding@resend.dev>',
      to:      [email],
      subject: `Your Karman verification code: ${otp}`,
      html: `<!DOCTYPE html>
<html>
<body style="font-family:Arial,sans-serif;max-width:480px;margin:0 auto;padding:24px;color:#1a1a2e;background:#f8f9fb;">
  <div style="background:#0A2540;padding:24px 32px;border-radius:10px 10px 0 0;text-align:center;">
    <div style="color:white;font-size:18px;font-weight:700;letter-spacing:-.3px;">Karman</div>
    <div style="color:rgba(255,255,255,.6);font-size:13px;margin-top:4px;">Corporate Services Singapore</div>
  </div>
  <div style="background:#fff;padding:36px 32px;border:1px solid #e1e4ea;border-top:none;border-radius:0 0 10px 10px;">
    <p style="font-size:15px;color:#6B7280;margin:0 0 24px;">Here is your one-time verification code to complete your onboarding:</p>
    <div style="text-align:center;margin:0 0 28px;">
      <div style="display:inline-block;background:#EBF3FD;border:2px solid #1A6BCC;border-radius:12px;padding:18px 40px;">
        <span style="font-size:36px;font-weight:800;letter-spacing:10px;color:#0A2540;font-family:monospace;">${otp}</span>
      </div>
    </div>
    <p style="font-size:13px;color:#9AA5B4;text-align:center;margin:0 0 4px;">Valid for <strong>10 minutes</strong>. Do not share this code.</p>
    <p style="font-size:13px;color:#9AA5B4;text-align:center;margin:0;">If you didn't request this, you can safely ignore this email.</p>
  </div>
  <p style="font-size:12px;color:#9AA5B4;text-align:center;margin-top:20px;">© 2025 Karman Corporate Services Pte Ltd · Singapore</p>
</body>
</html>`,
    }),
  });

  if (!emailRes.ok) {
    const err = await emailRes.json();
    console.error('[Karman OTP] Resend error:', err);
    return res.status(502).json({ error: 'Failed to send verification email. Please try again.' });
  }

  return res.status(200).json({ token });
};
