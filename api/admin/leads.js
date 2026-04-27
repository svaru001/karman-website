const { requireAuth, getLeads, setLeads, SEED } = require('./_lib');

function genId() {
  return Date.now().toString(36) + Math.random().toString(36).slice(2, 7);
}

module.exports = async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Headers', 'Authorization, Content-Type');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  if (req.method === 'OPTIONS') return res.status(200).end();
  if (!requireAuth(req, res)) return;

  // GET — list all leads (auto-seed if empty)
  if (req.method === 'GET') {
    let leads = await getLeads();
    if (!leads) {
      leads = SEED;
      await setLeads(leads);
    }
    leads = [...leads].sort((a, b) => new Date(b.date) - new Date(a.date));
    return res.status(200).json({ leads });
  }

  // POST — create new lead
  if (req.method === 'POST') {
    const { name, company, email, phone, date, type, status, comments, source } = req.body || {};
    if (!name) return res.status(400).json({ error: 'name required' });

    let leads = await getLeads();
    if (!leads) leads = [...SEED];

    const lead = {
      id: genId(),
      name: name.trim(),
      company: (company || '').trim(),
      email: (email || '').trim(),
      phone: (phone || '').trim(),
      date: date || new Date().toISOString().slice(0, 10),
      type: type || 'Prospect',
      status: status || 'Active',
      comments: (comments || '').trim(),
      source: source || 'manual',
      createdAt: Date.now(),
    };

    leads.unshift(lead);
    await setLeads(leads);
    return res.status(201).json({ lead });
  }

  return res.status(405).end();
};
