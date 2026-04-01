/* ─────────────────────────────────────────────
   KARMAN — Tool Result Email Handler
   POST /api/send-result
   Sends PDF to user + lead notification to admin.
   Requires env vars: RESEND_API_KEY, ADMIN_EMAIL
───────────────────────────────────────────── */

export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).end();

  const { toolId, userName, userEmail, subject, pdfBase64, adminSummary } = req.body;
  const key   = process.env.RESEND_API_KEY;
  const admin = process.env.ADMIN_EMAIL || 'hello@karman.com.sg';

  if (!key) return res.status(500).json({ error: 'Email service not configured' });

  const send = (payload) =>
    fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${key}`, 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

  // ── Email to user with PDF attachment ──
  const userRes = await send({
    from: 'Karman Corporate Services <hello@karman.com.sg>',
    to: [userEmail],
    subject,
    html: buildUserHtml(userName, toolId),
    attachments: pdfBase64 ? [{
      filename: `karman-${toolId.replace(/([A-Z])/g, '-$1').toLowerCase()}.pdf`,
      content: pdfBase64
    }] : undefined
  });

  if (!userRes.ok) {
    const err = await userRes.json();
    return res.status(502).json({ error: err.message || 'Failed to send email' });
  }

  // ── Lead notification to admin ──
  await send({
    from: 'Karman Website <hello@karman.com.sg>',
    to: [admin],
    subject: `[Lead] ${userName} — ${TOOL_NAMES[toolId] || toolId}`,
    html: buildAdminHtml(userName, userEmail, toolId, adminSummary)
  });

  return res.status(200).json({ ok: true });
}

const TOOL_NAMES = {
  businessStructure:  'Business Structure Recommender',
  costCalculator:     'Cost Calculator',
  eligibilityChecker: 'Eligibility Checker',
  timelineVisualizer: 'Timeline Visualizer',
  documentChecklist:  'Document Checklist'
};

function buildUserHtml(name, toolId) {
  const toolName = TOOL_NAMES[toolId] || 'Report';
  return `<!DOCTYPE html>
<html>
<body style="font-family:Arial,sans-serif;max-width:600px;margin:0 auto;padding:0;color:#1a1a2e;background:#f0f2f5;">
  <div style="background:#0A2540;padding:28px 36px;border-radius:8px 8px 0 0;">
    <div style="color:white;font-size:22px;font-weight:700;letter-spacing:-0.5px;">Karman</div>
    <div style="color:rgba(255,255,255,0.55);font-size:12px;margin-top:3px;letter-spacing:1px;text-transform:uppercase;">Corporate Services Singapore</div>
  </div>
  <div style="background:white;padding:36px;border:1px solid #e1e4ea;border-top:none;border-radius:0 0 8px 8px;">
    <p style="font-size:17px;color:#0A2540;font-weight:600;margin:0 0 10px;">Hi ${name},</p>
    <p style="color:#374151;line-height:1.7;margin:0 0 20px;">
      Thank you for using the Karman <strong>${toolName}</strong>. Your personalised report is attached to this email as a PDF.
    </p>
    <div style="background:#EBF3FD;border-left:4px solid #0A2540;padding:18px 20px;margin:0 0 28px;border-radius:0 6px 6px 0;">
      <p style="color:#0A2540;font-weight:700;margin:0 0 6px;font-size:14px;">Ready to take the next step?</p>
      <p style="color:#374151;margin:0;font-size:13px;line-height:1.6;">
        Our corporate services advisors are available for a free 30-minute consultation. No obligation — just expert guidance tailored to your situation.
      </p>
    </div>
    <a href="https://www.karman.com.sg/#contact"
       style="display:inline-block;background:#0A2540;color:white;padding:13px 28px;border-radius:6px;text-decoration:none;font-weight:700;font-size:14px;letter-spacing:0.2px;">
      Book a free consultation →
    </a>
    <hr style="border:none;border-top:1px solid #e1e4ea;margin:32px 0 20px;" />
    <p style="color:#9AA5B4;font-size:11px;line-height:1.7;margin:0;">
      Karman Corporate Services Pte Ltd · 1 Raffles Place #20-61, Singapore 048616<br/>
      <a href="mailto:hello@karman.com.sg" style="color:#0066CC;text-decoration:none;">hello@karman.com.sg</a> ·
      <a href="tel:+6561234567" style="color:#0066CC;text-decoration:none;">+65 6123 4567</a>
    </p>
  </div>
</body>
</html>`;
}

function buildAdminHtml(name, email, toolId, summary) {
  const toolName = TOOL_NAMES[toolId] || toolId;
  const summaryRows = summary
    ? summary.split('\n').map(line => {
        const [k, ...v] = line.split(':');
        return `<tr>
          <td style="padding:8px 12px;border:1px solid #ddd;font-weight:600;background:#f9fafb;white-space:nowrap;">${k}</td>
          <td style="padding:8px 12px;border:1px solid #ddd;">${v.join(':').trim()}</td>
        </tr>`;
      }).join('')
    : '';

  return `<!DOCTYPE html>
<html>
<body style="font-family:Arial,sans-serif;max-width:640px;margin:0 auto;padding:24px;color:#1a1a2e;">
  <div style="background:#0A2540;padding:20px 28px;border-radius:6px 6px 0 0;">
    <div style="color:white;font-size:16px;font-weight:700;">Karman — New Lead</div>
  </div>
  <div style="background:white;padding:28px;border:1px solid #ddd;border-top:none;border-radius:0 0 6px 6px;">
    <h2 style="margin:0 0 16px;color:#0A2540;font-size:18px;">${name} used the ${toolName}</h2>
    <table style="border-collapse:collapse;width:100%;font-size:14px;margin-bottom:20px;">
      <tr>
        <td style="padding:8px 12px;border:1px solid #ddd;font-weight:600;background:#f9fafb;">Name</td>
        <td style="padding:8px 12px;border:1px solid #ddd;">${name}</td>
      </tr>
      <tr>
        <td style="padding:8px 12px;border:1px solid #ddd;font-weight:600;background:#f9fafb;">Email</td>
        <td style="padding:8px 12px;border:1px solid #ddd;"><a href="mailto:${email}" style="color:#0066CC;">${email}</a></td>
      </tr>
      <tr>
        <td style="padding:8px 12px;border:1px solid #ddd;font-weight:600;background:#f9fafb;">Tool</td>
        <td style="padding:8px 12px;border:1px solid #ddd;">${toolName}</td>
      </tr>
      ${summaryRows}
    </table>
    <a href="mailto:${email}" style="background:#0A2540;color:white;padding:10px 22px;border-radius:6px;text-decoration:none;font-weight:600;font-size:13px;">
      Reply to ${name} →
    </a>
  </div>
</body>
</html>`;
}
