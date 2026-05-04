/* ─────────────────────────────────────────────
   KARMAN — Send Template via Resend (email-gated download)
   POST /api/send-template
   Body: { name, email, slug }
   - Emails the template file (as attachment + download link) to the user
   - Sends lead notification to admin
───────────────────────────────────────────── */

const fs = require('fs');
const path = require('path');

const ADMIN_EMAIL = process.env.ADMIN_EMAIL || 'sanket.varu@gmail.com';

let TEMPLATES_INDEX = null;
function loadIndex() {
  if (TEMPLATES_INDEX) return TEMPLATES_INDEX;
  try {
    const p = path.join(process.cwd(), 'templates', '_templates.json');
    TEMPLATES_INDEX = JSON.parse(fs.readFileSync(p, 'utf8'));
  } catch (e) {
    TEMPLATES_INDEX = { templates: [] };
  }
  return TEMPLATES_INDEX;
}

function loadTemplateBody(slug) {
  const safe = String(slug || '').replace(/[^a-z0-9-]/gi, '');
  if (!safe) return null;
  try {
    const p = path.join(process.cwd(), 'templates', '_files', `${safe}.txt`);
    return fs.readFileSync(p, 'utf8');
  } catch (e) {
    return null;
  }
}

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).end();

  const { name, email, slug } = req.body || {};
  const key = process.env.RESEND_API_KEY;

  if (!key) return res.status(500).json({ error: 'Email service not configured' });
  if (!name || !String(name).trim()) return res.status(400).json({ error: 'Name required' });
  if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    return res.status(400).json({ error: 'Valid email address required' });
  }
  if (!slug) return res.status(400).json({ error: 'Template slug required' });

  const index = loadIndex();
  const template = (index.templates || []).find(t => t.slug === slug);
  if (!template) return res.status(404).json({ error: 'Template not found' });

  const body = loadTemplateBody(slug);
  if (!body) return res.status(404).json({ error: 'Template file not found' });

  const filename = `${slug}.txt`;
  const downloadUrl = `https://karman.com.sg/templates/_files/${filename}`;
  const pageUrl = `https://karman.com.sg/templates/${slug}`;
  const attachmentB64 = Buffer.from(body, 'utf8').toString('base64');

  // 1. Send template to user
  const userRes = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${key}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({
      from: 'Karman <onboarding@resend.dev>',
      to: [email],
      subject: `Your ${template.title} from Karman`,
      html: buildUserEmail({ name, template, downloadUrl, pageUrl }),
      attachments: [
        { filename, content: attachmentB64 }
      ],
    })
  });

  if (!userRes.ok) {
    const err = await userRes.json().catch(() => ({}));
    console.error('[Karman send-template] User email failed:', err);
    return res.status(502).json({ error: 'Failed to send template. Please try again.' });
  }

  // 2. Notify admin (lead capture)
  await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${key}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({
      from: 'Karman Website <onboarding@resend.dev>',
      to: [ADMIN_EMAIL],
      subject: `[Template Lead] ${name} downloaded ${template.title}`,
      html: buildAdminEmail({ name, email, template }),
    })
  }).catch(e => console.error('[Karman send-template] Admin notify failed:', e));

  return res.status(200).json({ ok: true });
};


function buildUserEmail({ name, template, downloadUrl, pageUrl }) {
  return `<!DOCTYPE html>
<html>
<body style="font-family:Arial,sans-serif;max-width:560px;margin:0 auto;padding:24px;color:#1a1a2e;background:#f8f9fb;">
  <div style="background:#0A2540;padding:24px 32px;border-radius:10px 10px 0 0;">
    <div style="color:white;font-size:18px;font-weight:700;letter-spacing:-.3px;">Karman</div>
    <div style="color:rgba(255,255,255,.6);font-size:13px;margin-top:4px;">Corporate Services Singapore</div>
  </div>
  <div style="background:#fff;padding:32px;border:1px solid #e1e4ea;border-top:none;border-radius:0 0 10px 10px;">
    <p style="font-size:16px;color:#0A2540;margin:0 0 16px;">Hi ${escapeHtml(name)},</p>
    <p style="font-size:15px;color:#374151;line-height:1.6;margin:0 0 18px;">Here's the <strong>${escapeHtml(template.title)}</strong> you requested. The file is attached to this email and you can also download it directly:</p>

    <div style="text-align:center;margin:24px 0;">
      <a href="${downloadUrl}" style="display:inline-block;background:#0d4567;color:#fff;padding:13px 28px;border-radius:8px;text-decoration:none;font-weight:700;font-size:15px;">Download template (.txt)</a>
    </div>

    <p style="font-size:14px;color:#6B7280;line-height:1.6;margin:0 0 18px;"><strong>How to use it:</strong> Open in Word, Google Docs, or any text editor. Replace the bracketed placeholders ([COMPANY NAME], [DD Month YYYY], etc.) with your details. Save as .docx if you want clean formatting.</p>

    <p style="font-size:14px;color:#6B7280;line-height:1.6;margin:0 0 18px;">Full guidance and FAQs on the template page: <a href="${pageUrl}" style="color:#0d4567;">${pageUrl}</a></p>

    <hr style="border:none;border-top:1px solid #e1e4ea;margin:24px 0;" />

    <p style="font-size:14px;color:#374151;line-height:1.6;margin:0 0 12px;"><strong>Need a corporate secretary to handle the filing?</strong></p>
    <p style="font-size:14px;color:#6B7280;line-height:1.6;margin:0 0 12px;">Karman handles ACRA filings, IRAS stamp duty, statutory register updates, and resolution preparation as part of our corporate secretarial service from S$50/month. Reply to this email or visit <a href="https://karman.com.sg/#contact" style="color:#0d4567;">karman.com.sg</a>.</p>

    <p style="font-size:13px;color:#9AA5B4;line-height:1.5;margin:24px 0 0;">This template is provided as-is for general guidance and does not constitute legal advice. For complex transactions, consult your corporate secretary or legal counsel.</p>
  </div>
  <p style="font-size:12px;color:#9AA5B4;text-align:center;margin-top:20px;">© 2026 Karman Corporate Services Pte Ltd · Singapore · UEN 202012889R</p>
</body>
</html>`;
}

function buildAdminEmail({ name, email, template }) {
  return `<!DOCTYPE html>
<html>
<body style="font-family:Arial,sans-serif;max-width:560px;margin:0 auto;padding:24px;color:#1a1a2e;">
  <div style="background:#0A2540;padding:20px 28px;border-radius:6px 6px 0 0;">
    <div style="color:white;font-size:16px;font-weight:700;">Karman — Template Lead</div>
    <div style="color:rgba(255,255,255,0.55);font-size:12px;margin-top:4px;">${escapeHtml(template.title)}</div>
  </div>
  <div style="background:white;padding:24px 28px;border:1px solid #ddd;border-top:none;border-radius:0 0 6px 6px;">
    <table style="border-collapse:collapse;width:100%;font-size:14px;">
      <tr><td style="padding:8px 12px;border:1px solid #e1e4ea;font-weight:600;background:#f9fafb;width:130px;">Name</td><td style="padding:8px 12px;border:1px solid #e1e4ea;">${escapeHtml(name)}</td></tr>
      <tr><td style="padding:8px 12px;border:1px solid #e1e4ea;font-weight:600;background:#f9fafb;">Email</td><td style="padding:8px 12px;border:1px solid #e1e4ea;"><a href="mailto:${escapeHtml(email)}" style="color:#0066CC;">${escapeHtml(email)}</a></td></tr>
      <tr><td style="padding:8px 12px;border:1px solid #e1e4ea;font-weight:600;background:#f9fafb;">Template</td><td style="padding:8px 12px;border:1px solid #e1e4ea;">${escapeHtml(template.title)}</td></tr>
      <tr><td style="padding:8px 12px;border:1px solid #e1e4ea;font-weight:600;background:#f9fafb;">Category</td><td style="padding:8px 12px;border:1px solid #e1e4ea;">${escapeHtml(template.category)}</td></tr>
      <tr><td style="padding:8px 12px;border:1px solid #e1e4ea;font-weight:600;background:#f9fafb;">Time</td><td style="padding:8px 12px;border:1px solid #e1e4ea;">${new Date().toISOString()}</td></tr>
    </table>
    <p style="margin-top:20px;font-size:13px;color:#6B7280;">A new lead — they downloaded a corporate template and likely need filing or secretarial help. Consider reaching out within 48 hours.</p>
    <a href="mailto:${escapeHtml(email)}?subject=Re: Your ${encodeURIComponent(template.title)} download" style="display:inline-block;background:#0A2540;color:white;padding:11px 24px;border-radius:6px;text-decoration:none;font-weight:600;font-size:13px;margin-top:8px;">Reply to ${escapeHtml(name)} →</a>
  </div>
</body>
</html>`;
}

function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, c => ({ '&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;', "'":'&#39;' }[c]));
}
