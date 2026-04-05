/* ─────────────────────────────────────────────
   KARMAN — Contact Form Handler
   POST /api/contact
   Sends enquiry notification to Sanket's Gmail.
   No custom domain DNS required.
───────────────────────────────────────────── */

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).end();

  const { name, email, phone, service, message } = req.body;
  const key = process.env.RESEND_API_KEY;

  if (!key) return res.status(500).json({ error: 'Email service not configured' });
  if (!name) return res.status(400).json({ error: 'Name required' });

  const notifyRes = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${key}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({
      from: 'Karman Website <onboarding@resend.dev>',
      to: ['sanket.varu@gmail.com'],
      subject: `[Enquiry] ${name}${service ? ' — ' + service : ''}`,
      html: `<!DOCTYPE html>
<html>
<body style="font-family:Arial,sans-serif;max-width:640px;margin:0 auto;padding:24px;color:#1a1a2e;">
  <div style="background:#0A2540;padding:20px 28px;border-radius:6px 6px 0 0;">
    <div style="color:white;font-size:16px;font-weight:700;">Karman — New Website Enquiry</div>
  </div>
  <div style="background:white;padding:28px;border:1px solid #ddd;border-top:none;border-radius:0 0 6px 6px;">
    <table style="border-collapse:collapse;width:100%;font-size:14px;margin-bottom:20px;">
      <tr><td style="padding:10px 14px;border:1px solid #e1e4ea;font-weight:600;background:#f9fafb;width:120px;">Name</td><td style="padding:10px 14px;border:1px solid #e1e4ea;">${name}</td></tr>
      <tr><td style="padding:10px 14px;border:1px solid #e1e4ea;font-weight:600;background:#f9fafb;">Email</td><td style="padding:10px 14px;border:1px solid #e1e4ea;">${email ? `<a href="mailto:${email}" style="color:#0066CC;">${email}</a>` : '—'}</td></tr>
      <tr><td style="padding:10px 14px;border:1px solid #e1e4ea;font-weight:600;background:#f9fafb;">Phone</td><td style="padding:10px 14px;border:1px solid #e1e4ea;">${phone || '—'}</td></tr>
      <tr><td style="padding:10px 14px;border:1px solid #e1e4ea;font-weight:600;background:#f9fafb;">Service</td><td style="padding:10px 14px;border:1px solid #e1e4ea;">${service || '—'}</td></tr>
      <tr><td style="padding:10px 14px;border:1px solid #e1e4ea;font-weight:600;background:#f9fafb;">Message</td><td style="padding:10px 14px;border:1px solid #e1e4ea;white-space:pre-wrap;">${message || '—'}</td></tr>
    </table>
    ${email ? `<a href="mailto:${email}?subject=Re: Your Karman enquiry" style="background:#0A2540;color:white;padding:11px 24px;border-radius:6px;text-decoration:none;font-weight:600;font-size:13px;">Reply to ${name} →</a>` : ''}
  </div>
</body>
</html>`
    })
  });

  if (!notifyRes.ok) {
    const err = await notifyRes.json();
    return res.status(502).json({ error: err.message || 'Failed to send' });
  }

  return res.status(200).json({ ok: true });
}
