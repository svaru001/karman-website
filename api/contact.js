/* ─────────────────────────────────────────────
   KARMAN — Contact Form Handler
   POST /api/contact
   Sends enquiry to admin + confirmation to user.
   Requires env vars: RESEND_API_KEY, ADMIN_EMAIL
───────────────────────────────────────────── */

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).end();

  const { name, email, service, message } = req.body;
  const key   = process.env.RESEND_API_KEY;
  const admin = process.env.ADMIN_EMAIL || 'hello@karman.com.sg';

  if (!key) return res.status(500).json({ error: 'Email service not configured' });
  if (!name || !email) return res.status(400).json({ error: 'Name and email required' });

  const send = (payload) =>
    fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${key}`, 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

  // ── Notify admin ──
  const adminRes = await send({
    from: 'Karman Website <hello@karman.com.sg>',
    to: [admin],
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
      <tr><td style="padding:10px 14px;border:1px solid #e1e4ea;font-weight:600;background:#f9fafb;">Email</td><td style="padding:10px 14px;border:1px solid #e1e4ea;"><a href="mailto:${email}" style="color:#0066CC;">${email}</a></td></tr>
      <tr><td style="padding:10px 14px;border:1px solid #e1e4ea;font-weight:600;background:#f9fafb;">Service</td><td style="padding:10px 14px;border:1px solid #e1e4ea;">${service || '—'}</td></tr>
      <tr><td style="padding:10px 14px;border:1px solid #e1e4ea;font-weight:600;background:#f9fafb;">Message</td><td style="padding:10px 14px;border:1px solid #e1e4ea;white-space:pre-wrap;">${message || '—'}</td></tr>
    </table>
    <a href="mailto:${email}?subject=Re: Your Karman enquiry" style="background:#0A2540;color:white;padding:11px 24px;border-radius:6px;text-decoration:none;font-weight:600;font-size:13px;">Reply to ${name} →</a>
  </div>
</body>
</html>`
  });

  if (!adminRes.ok) {
    const err = await adminRes.json();
    return res.status(502).json({ error: err.message || 'Failed to send' });
  }

  // ── Confirmation to user ──
  await send({
    from: 'Karman Corporate Services <hello@karman.com.sg>',
    to: [email],
    subject: 'We received your enquiry — Karman Corporate Services',
    html: `<!DOCTYPE html>
<html>
<body style="font-family:Arial,sans-serif;max-width:600px;margin:0 auto;padding:0;background:#f0f2f5;">
  <div style="background:#0A2540;padding:28px 36px;border-radius:8px 8px 0 0;">
    <div style="color:white;font-size:22px;font-weight:700;letter-spacing:-0.5px;">Karman</div>
    <div style="color:rgba(255,255,255,0.55);font-size:12px;margin-top:3px;letter-spacing:1px;text-transform:uppercase;">Corporate Services Singapore</div>
  </div>
  <div style="background:white;padding:36px;border:1px solid #e1e4ea;border-top:none;border-radius:0 0 8px 8px;">
    <p style="font-size:17px;color:#0A2540;font-weight:600;margin:0 0 12px;">Hi ${name},</p>
    <p style="color:#374151;line-height:1.7;margin:0 0 16px;">
      Thank you for reaching out${service ? ' about <strong>' + service + '</strong>' : ''}. We've received your enquiry and one of our advisors will be in touch within <strong>1 business day</strong>.
    </p>
    <p style="color:#374151;line-height:1.7;margin:0 0 28px;">
      If your matter is urgent, call us directly at <a href="tel:+6561234567" style="color:#0A2540;font-weight:600;">+65 6123 4567</a> (Mon–Fri, 9am–6pm SGT).
    </p>
    <div style="background:#EBF3FD;border-left:4px solid #0A2540;padding:16px 20px;margin:0 0 28px;border-radius:0 6px 6px 0;">
      <p style="color:#0A2540;font-weight:700;margin:0 0 6px;font-size:14px;">While you wait, try our free tools</p>
      <p style="color:#374151;margin:0;font-size:13px;line-height:1.6;">Estimate your fees, check your eligibility, or see the incorporation timeline — no sign-up required.</p>
    </div>
    <a href="https://www.karman.com.sg/tools/" style="display:inline-block;background:#0A2540;color:white;padding:13px 28px;border-radius:6px;text-decoration:none;font-weight:700;font-size:14px;">Explore free tools →</a>
    <hr style="border:none;border-top:1px solid #e1e4ea;margin:32px 0 20px;" />
    <p style="color:#9AA5B4;font-size:11px;line-height:1.7;margin:0;">
      Karman Corporate Services Pte Ltd · 1 Raffles Place #20-61, Singapore 048616<br/>
      <a href="mailto:hello@karman.com.sg" style="color:#0066CC;text-decoration:none;">hello@karman.com.sg</a> · <a href="tel:+6561234567" style="color:#0066CC;text-decoration:none;">+65 6123 4567</a>
    </p>
  </div>
</body>
</html>`
  });

  return res.status(200).json({ ok: true });
}
