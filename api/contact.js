/* ─────────────────────────────────────────────
   KARMAN — Contact Form Handler
   POST /api/contact
   Sends enquiry notification to Sanket's Gmail.
   No custom domain DNS required.
───────────────────────────────────────────── */

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).end();

  const { name, email, phone, service, message, source, entityType, stage, country, company, vcc } = req.body;
  const key = process.env.RESEND_API_KEY;

  if (!key) return res.status(500).json({ error: 'Email service not configured' });
  if (!name) return res.status(400).json({ error: 'Name required' });

  const isOnboarding = source === 'onboarding';
  const subject = isOnboarding
    ? `[Onboarding] ${name} — ${entityType === 'vcc' ? 'VCC / Fund' : 'Private Company'}`
    : `[Enquiry] ${name}${service ? ' — ' + service : ''}`;

  const html = isOnboarding
    ? buildOnboardingEmail({ name, email, phone, service, entityType, stage, country, company, vcc })
    : buildGenericEmail({ name, email, phone, service, message });

  const notifyRes = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${key}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({
      from: 'Karman Website <onboarding@resend.dev>',
      to: ['sanket.varu@gmail.com'],
      subject,
      html,
    })
  });

  if (!notifyRes.ok) {
    const err = await notifyRes.json();
    return res.status(502).json({ error: err.message || 'Failed to send' });
  }

  return res.status(200).json({ ok: true });
}

/* ── Helpers ── */

const td  = `style="padding:10px 14px;border:1px solid #e1e4ea;"`;
const th  = `style="padding:10px 14px;border:1px solid #e1e4ea;font-weight:600;background:#f9fafb;width:140px;white-space:nowrap;"`;
const row = (label, value) => value ? `<tr><td ${th}>${label}</td><td ${td}>${value}</td></tr>` : '';

const STAGE_LABELS    = { new: 'Starting fresh', existing: 'Already incorporated', foreign: 'Foreign expansion' };
const DIR_LABELS      = { yes: 'Yes', no: 'No — needs nominee', unsure: 'Not sure' };
const EMP_LABELS      = { 'yes-immediate': 'Yes, immediately', 'yes-later': 'Yes, later', no: 'No' };
const TL_LABELS       = { asap: 'ASAP', '1 month': '~1 month', '1-3 months': '1–3 months', '3+ months': '3+ months', exploring: 'Just exploring' };
const FUND_MGR_LABELS = { 'yes-licensed': 'Yes, MAS-licensed', 'yes-exempt': 'Yes, exempt (RFMC/A-CIS)', no: 'No — need one appointed', 'not sure': 'Not sure' };
const ADDR_LABELS     = { karman: "Karman's address", own: 'Own address' };

function sectionHeading(text) {
  return `<tr><td colspan="2" style="padding:14px 14px 8px;border:none;font-weight:700;font-size:13px;color:#0A2540;text-transform:uppercase;letter-spacing:0.5px;">${text}</td></tr>`;
}

function buildOnboardingEmail({ name, email, phone, service, entityType, stage, country, company, vcc }) {
  const entityLabel = entityType === 'vcc' ? 'VCC / Fund' : 'Private Company (Pte. Ltd.)';

  let detailRows = '';

  if (entityType === 'vcc' && vcc) {
    detailRows = `
      ${sectionHeading('VCC / Fund Details')}
      ${row('Entity type', entityLabel)}
      ${row('VCC name', vcc.name)}
      ${row('Fund type', vcc.fundType)}
      ${row('Strategy', vcc.strategy)}
      ${row('Expected AUM', vcc.aum)}
      ${row('Fund focus', vcc.description)}
      ${row('Directors', vcc.directors)}
      ${row('Fund manager', FUND_MGR_LABELS[vcc.fundManager] || vcc.fundManager)}
      ${row('FY end', vcc.fyEnd)}
      ${row('Timeline', TL_LABELS[vcc.timeline] || vcc.timeline)}
      ${row('Registered address', ADDR_LABELS[vcc.registeredAddress] || vcc.registeredAddress)}`;
  } else if (company) {
    detailRows = `
      ${sectionHeading('Company Details')}
      ${row('Entity type', entityLabel)}
      ${row('Company name', company.name)}
      ${row('Industry', company.industry)}
      ${row('Business description', company.description)}
      ${row('Directors', company.directors)}
      ${row('Shareholders', company.shareholders)}
      ${row('Share capital', company.shareCapital)}
      ${row('FY end', company.fyEnd)}
      ${row('Local director', DIR_LABELS[company.localDirector] || company.localDirector)}
      ${row('Employees in SG', EMP_LABELS[company.employees] || company.employees)}
      ${row('Timeline', TL_LABELS[company.timeline] || company.timeline)}
      ${row('Registered address', ADDR_LABELS[company.registeredAddress] || company.registeredAddress)}`;
  }

  return `<!DOCTYPE html>
<html>
<body style="font-family:Arial,sans-serif;max-width:640px;margin:0 auto;padding:24px;color:#1a1a2e;">
  <div style="background:#0A2540;padding:20px 28px;border-radius:6px 6px 0 0;">
    <div style="color:white;font-size:16px;font-weight:700;">Karman — New Onboarding Enquiry</div>
    <div style="color:rgba(255,255,255,0.55);font-size:12px;margin-top:4px;">${entityLabel}</div>
  </div>
  <div style="background:white;padding:28px;border:1px solid #ddd;border-top:none;border-radius:0 0 6px 6px;">
    <table style="border-collapse:collapse;width:100%;font-size:14px;margin-bottom:20px;">
      ${sectionHeading('Contact')}
      ${row('Name', name)}
      ${row('Email', email ? `<a href="mailto:${email}" style="color:#0066CC;">${email}</a>` : null)}
      ${row('Phone', phone)}
      ${row('Country', country)}
      ${row('Stage', STAGE_LABELS[stage] || stage)}
      ${detailRows}
      ${sectionHeading('Services Requested')}
      ${row('Services', service || '—')}
    </table>
    ${email ? `<a href="mailto:${email}?subject=Re: Your Karman onboarding enquiry" style="display:inline-block;background:#0A2540;color:white;padding:11px 24px;border-radius:6px;text-decoration:none;font-weight:600;font-size:13px;">Reply to ${name} →</a>` : ''}
  </div>
</body>
</html>`;
}

function buildGenericEmail({ name, email, phone, service, message }) {
  return `<!DOCTYPE html>
<html>
<body style="font-family:Arial,sans-serif;max-width:640px;margin:0 auto;padding:24px;color:#1a1a2e;">
  <div style="background:#0A2540;padding:20px 28px;border-radius:6px 6px 0 0;">
    <div style="color:white;font-size:16px;font-weight:700;">Karman — New Website Enquiry</div>
  </div>
  <div style="background:white;padding:28px;border:1px solid #ddd;border-top:none;border-radius:0 0 6px 6px;">
    <table style="border-collapse:collapse;width:100%;font-size:14px;margin-bottom:20px;">
      ${row('Name', name)}
      ${row('Email', email ? `<a href="mailto:${email}" style="color:#0066CC;">${email}</a>` : null)}
      ${row('Phone', phone)}
      ${row('Service', service)}
      <tr><td ${th}>Message</td><td style="padding:10px 14px;border:1px solid #e1e4ea;white-space:pre-wrap;">${message || '—'}</td></tr>
    </table>
    ${email ? `<a href="mailto:${email}?subject=Re: Your Karman enquiry" style="background:#0A2540;color:white;padding:11px 24px;border-radius:6px;text-decoration:none;font-weight:600;font-size:13px;">Reply to ${name} →</a>` : ''}
  </div>
</body>
</html>`;
}
