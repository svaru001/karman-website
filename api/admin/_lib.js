const crypto = require('crypto');

const SECRET = process.env.OTP_SECRET || 'karman-dev-secret';
const KV_URL = process.env.KV_REST_API_URL;
const KV_TOKEN = process.env.KV_REST_API_TOKEN;
const LEADS_KEY = 'karman:leads';

// ── Auth ──────────────────────────────────────────────────────────────────────

function createToken() {
  const payload = Buffer.from(JSON.stringify({
    sub: 'admin',
    iat: Date.now(),
    exp: Date.now() + 24 * 60 * 60 * 1000, // 24h
  })).toString('base64');
  const sig = crypto.createHmac('sha256', SECRET).update(payload).digest('hex');
  return `${payload}.${sig}`;
}

function verifyToken(token) {
  if (!token) return null;
  const dot = token.lastIndexOf('.');
  if (dot === -1) return null;
  const payload = token.slice(0, dot);
  const sig = token.slice(dot + 1);
  const expected = crypto.createHmac('sha256', SECRET).update(payload).digest('hex');
  if (sig !== expected) return null;
  try {
    const data = JSON.parse(Buffer.from(payload, 'base64').toString());
    if (data.exp < Date.now()) return null;
    return data;
  } catch { return null; }
}

function requireAuth(req, res) {
  const auth = req.headers.authorization || '';
  const token = auth.startsWith('Bearer ') ? auth.slice(7) : null;
  if (!verifyToken(token)) {
    res.status(401).json({ error: 'Unauthorized' });
    return false;
  }
  return true;
}

// ── Vercel KV (Upstash REST) ───────────────────────────────────────────────────

async function kvCmd(...args) {
  if (!KV_URL || !KV_TOKEN) return null;
  try {
    const r = await fetch(KV_URL, {
      method: 'POST',
      headers: { Authorization: `Bearer ${KV_TOKEN}`, 'Content-Type': 'application/json' },
      body: JSON.stringify(args),
    });
    const d = await r.json();
    return d.result !== undefined ? d.result : null;
  } catch { return null; }
}

async function getLeads() {
  const raw = await kvCmd('GET', LEADS_KEY);
  if (!raw) return null;
  try { return JSON.parse(raw); } catch { return null; }
}

async function setLeads(leads) {
  await kvCmd('SET', LEADS_KEY, JSON.stringify(leads));
}

// ── Seed Data ──────────────────────────────────────────────────────────────────

const SEED = [
  { id: '1', name: 'Ufuk Tas',      company: 'To be formed',                                              email: '', phone: '', date: '2026-04-23', type: 'Prospect',    status: 'Active',   comments: 'Meeting Scheduled',               source: 'backfill', createdAt: 1745366400000 },
  { id: '2', name: 'Eunbee',        company: 'WeMeetMobility',                                            email: '', phone: '', date: '2026-04-23', type: 'Prospect',    status: 'Active',   comments: 'Proposal Shared on 27th April',    source: 'backfill', createdAt: 1745366400000 },
  { id: '3', name: 'Jason Tan',     company: 'MCapital',                                                  email: '', phone: '', date: '2026-04-20', type: 'Partnership', status: 'Active',   comments: 'Need to schedule a meeting',       source: 'backfill', createdAt: 1745107200000 },
  { id: '4', name: 'Rendy',         company: 'KeepItYourself.com',                                        email: '', phone: '', date: '2026-04-12', type: 'Prospect',    status: 'Inactive', comments: 'Want to incorporate in Panama',    source: 'backfill', createdAt: 1744416000000 },
  { id: '5', name: 'Joyce Tan',     company: 'KEA Education Pte Ltd',                                     email: '', phone: '', date: '2026-04-08', type: 'Prospect',    status: 'Inactive', comments: 'Fees too high',                    source: 'backfill', createdAt: 1744070400000 },
  { id: '6', name: 'Ellen Long WJ', company: 'Shanghai Ruichuangtong Business Consulting Co., Ltd',       email: '', phone: '', date: '2026-04-20', type: 'Partnership', status: 'Active',   comments: 'Need to share whitelabel rates',   source: 'backfill', createdAt: 1745107200000 },
];

module.exports = { createToken, verifyToken, requireAuth, getLeads, setLeads, SEED };
