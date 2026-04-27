const { requireAuth, getLeads, setLeads, SEED } = require('./_lib');

module.exports = async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Headers', 'Authorization, Content-Type');
  res.setHeader('Access-Control-Allow-Methods', 'PATCH, DELETE, OPTIONS');
  if (req.method === 'OPTIONS') return res.status(200).end();
  if (!requireAuth(req, res)) return;

  const { id } = req.query;
  if (!id) return res.status(400).json({ error: 'id required' });

  let leads = await getLeads();
  if (!leads) leads = [...SEED];

  const idx = leads.findIndex(l => l.id === id);
  if (idx === -1) return res.status(404).json({ error: 'Lead not found' });

  // PATCH — update fields
  if (req.method === 'PATCH') {
    const allowed = ['name', 'company', 'email', 'phone', 'date', 'type', 'status', 'comments'];
    const body = req.body || {};
    const lead = { ...leads[idx] };
    for (const key of allowed) {
      if (body[key] !== undefined) lead[key] = typeof body[key] === 'string' ? body[key].trim() : body[key];
    }
    lead.updatedAt = Date.now();
    leads[idx] = lead;
    await setLeads(leads);
    return res.status(200).json({ lead });
  }

  // DELETE — remove lead
  if (req.method === 'DELETE') {
    leads.splice(idx, 1);
    await setLeads(leads);
    return res.status(200).json({ ok: true });
  }

  return res.status(405).end();
};
