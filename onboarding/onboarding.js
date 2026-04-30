/* ─────────────────────────────────────────────
   KARMAN — Onboarding Flow JS
   Steps: 1=About You · 2=Company · 3=Services · 4=Email OTP · 5=Success
───────────────────────────────────────────── */

/* ══════════════════════════════════════════
   1. HEX CANVAS BACKGROUND
══════════════════════════════════════════ */
(function initCanvas() {
  const canvas = document.getElementById('hexCanvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  let W, H, nodes, animId;

  function resize() {
    W = canvas.width  = canvas.offsetWidth;
    H = canvas.height = canvas.offsetHeight;
    if (!nodes) buildNodes();
  }

  function buildNodes() {
    const count = Math.max(14, Math.floor((W * H) / 18000));
    nodes = Array.from({ length: count }, () => {
      const type    = Math.random() < .25 ? 'filled' : Math.random() < .5 ? 'outline' : 'dot';
      const isTeal  = Math.random() < .25;
      return {
        x: Math.random() * W, y: Math.random() * H,
        vx: (Math.random() - .5) * .28, vy: (Math.random() - .5) * .28,
        r:     type === 'dot' ? Math.random() * 2 + 1 : Math.random() * 18 + 8,
        alpha: Math.random() * .35 + .05,
        phase: Math.random() * Math.PI * 2,
        speed: Math.random() * .012 + .006,
        color: isTeal ? '#00C9A7' : '#1A6BCC',
        type,
      };
    });
  }

  function hexPath(cx, cy, r) {
    ctx.beginPath();
    for (let i = 0; i < 6; i++) {
      const a = (Math.PI / 3) * i - Math.PI / 6;
      i === 0 ? ctx.moveTo(cx + r * Math.cos(a), cy + r * Math.sin(a))
              : ctx.lineTo(cx + r * Math.cos(a), cy + r * Math.sin(a));
    }
    ctx.closePath();
  }

  function hex2(n) { return Math.floor(n * 255).toString(16).padStart(2, '0'); }

  function draw(ts) {
    ctx.clearRect(0, 0, W, H);
    const g = ctx.createLinearGradient(0, 0, W, H);
    g.addColorStop(0, '#0A2540'); g.addColorStop(1, '#0d2f4d');
    ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);

    // Connection lines
    for (let i = 0; i < nodes.length; i++) {
      for (let j = i + 1; j < nodes.length; j++) {
        const dx = nodes[i].x - nodes[j].x, dy = nodes[i].y - nodes[j].y;
        const d  = Math.sqrt(dx * dx + dy * dy);
        if (d < 140) {
          ctx.beginPath(); ctx.moveTo(nodes[i].x, nodes[i].y); ctx.lineTo(nodes[j].x, nodes[j].y);
          ctx.strokeStyle = `rgba(26,107,204,${(1 - d / 140) * .12})`; ctx.lineWidth = .8; ctx.stroke();
        }
      }
    }

    nodes.forEach(n => {
      const a = n.alpha + Math.sin(ts * n.speed + n.phase) * (n.alpha * .4);
      if (n.type === 'dot') {
        ctx.beginPath(); ctx.arc(n.x, n.y, n.r, 0, Math.PI * 2);
        ctx.fillStyle = n.color + hex2(a); ctx.fill();
      } else if (n.type === 'outline') {
        hexPath(n.x, n.y, n.r);
        ctx.strokeStyle = n.color + hex2(a); ctx.lineWidth = 1.2; ctx.stroke();
      } else {
        hexPath(n.x, n.y, n.r);
        ctx.fillStyle = n.color + hex2(a * .31); ctx.fill();
        hexPath(n.x, n.y, n.r);
        ctx.strokeStyle = n.color + hex2(a * .7); ctx.lineWidth = 1; ctx.stroke();
      }
      n.x += n.vx; n.y += n.vy;
      if (n.x < -n.r * 2) n.x = W + n.r; if (n.x > W + n.r * 2) n.x = -n.r;
      if (n.y < -n.r * 2) n.y = H + n.r; if (n.y > H + n.r * 2) n.y = -n.r;
    });

    animId = requestAnimationFrame(draw);
  }

  window.addEventListener('resize', () => { cancelAnimationFrame(animId); resize(); requestAnimationFrame(draw); });
  resize();
  requestAnimationFrame(draw);
})();


/* ══════════════════════════════════════════
   2. STATE
══════════════════════════════════════════ */
const state = {
  step: 1,
  // Step 1
  firstName: '', lastName: '', email: '', phone: '', country: 'SG', stage: '',
  // Step 2 — entity type
  entityType: '',       // 'private' or 'vcc'
  // Step 2 — private company
  companyName: '', industry: '', bizDesc: '', directors: '', shareholders: '',
  shareCapital: '', fyEnd: '', localDir: '', employees: '', timeline: '', registeredAddress: '',
  // Step 2 — VCC / Fund
  vccName: '', fundType: '', fundStrategy: '', fundAum: '', fundDesc: '',
  vccDirectors: '', fundManager: '', vccFyEnd: '', vccTimeline: '', vccRegisteredAddress: '',
  // Step 3
  services: new Set(),
};
const TOTAL_STEPS = 3;


/* ══════════════════════════════════════════
   3. SERVICES DATA
══════════════════════════════════════════ */
const SERVICES_PRIVATE = [
  { id: 'incorporation', icon: 'building-2', title: 'Company Incorporation',  desc: 'Register your Pte. Ltd. with ACRA' },
  { id: 'secretary',    icon: 'clipboard-list', title: 'Corporate Secretary',    desc: 'Annual compliance & statutory filings' },
  { id: 'accounting',  icon: 'bar-chart-3', title: 'Accounting & Bookkeeping', desc: 'Monthly financials & reports' },
  { id: 'tax',         icon: 'file-text', title: 'Corporate Tax Filing',    desc: 'ECI, Form C-S & tax planning' },
  { id: 'gst',         icon: 'receipt', title: 'GST Registration & Filing', desc: 'GST reg & quarterly F5 returns' },
  { id: 'payroll',     icon: 'wallet', title: 'Payroll Services',        desc: 'CPF, payslips & IR8A filing' },
  { id: 'visa',        icon: 'plane',  title: 'Employment Pass',         desc: 'Work visa for foreign directors' },
  { id: 'nominee',     icon: 'user', title: 'Nominee Director',        desc: 'Fulfil local director requirement' },
];

const SERVICES_VCC = [
  { id: 'vcc-setup',      icon: 'landmark', title: 'VCC Incorporation',      desc: 'Register your VCC with ACRA & MAS' },
  { id: 'fund-admin',     icon: 'clipboard-list', title: 'Fund Administration',  desc: 'NAV calculation, investor reporting' },
  { id: 'secretary',      icon: 'clipboard-list', title: 'Corporate Secretary',  desc: 'Annual compliance & statutory filings' },
  { id: 'accounting',     icon: 'bar-chart-3', title: 'Fund Accounting',       desc: 'Financial statements & audit-ready books' },
  { id: 'tax',            icon: 'file-text', title: 'Tax Filing & Advisory',  desc: 'VCC tax incentives, S13R/S13X claims' },
  { id: 'nominee',        icon: 'user', title: 'Nominee Director',          desc: 'Fulfil local director requirement' },
  { id: 'aml-compliance', icon: 'shield', title: 'AML / KYC Compliance',    desc: 'Investor due diligence & ongoing monitoring' },
  { id: 'visa',           icon: 'plane', title: 'Employment Pass',           desc: 'Work visa for foreign fund managers' },
];

// Keep a unified SERVICES reference for the success summary
let SERVICES = SERVICES_PRIVATE;


/* ══════════════════════════════════════════
   4. STEP TRANSITIONS
══════════════════════════════════════════ */
function goToStep(next, dir = 'forward') {
  const cur     = document.getElementById(`panel-${state.step}`);
  const nxt     = document.getElementById(`panel-${next}`);
  if (!nxt) return;
  const xOut = dir === 'forward' ? -32 : 32;
  const xIn  = dir === 'forward' ?  32 : -32;

  const isMobile = window.innerWidth <= 900;
  if (window.gsap && !isMobile) {
    gsap.timeline()
      .to(cur, { opacity: 0, x: xOut, duration: .26, ease: 'power2.in', onComplete: () => {
        cur.classList.add('ob-panel--hidden'); cur.style.cssText = '';
      }})
      .set(nxt, { x: xIn, opacity: 0 })
      .call(() => nxt.classList.remove('ob-panel--hidden'))
      .to(nxt, { opacity: 1, x: 0, duration: .3, ease: 'power2.out' });
  } else {
    cur.classList.add('ob-panel--hidden');
    nxt.classList.remove('ob-panel--hidden');
  }

  state.step = next;
  updateProgress();
  updateSidebar();
  setTimeout(() => {
    const isMobile = window.innerWidth <= 900;
    if (isMobile) {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    } else {
      const right = document.querySelector('.ob-right');
      if (right) right.scrollTop = 0;
    }
  }, 120);
}

function updateProgress() {
  const fill    = document.getElementById('progressFill');
  const counter = document.getElementById('stepCounter');
  if (state.step > TOTAL_STEPS) {
    fill.style.width = '100%';
    counter.textContent = 'Complete ✓';
  } else {
    fill.style.width = `${((state.step - 1) / TOTAL_STEPS) * 100}%`;
    counter.textContent = `Step ${state.step} of ${TOTAL_STEPS}`;
  }
}

function updateSidebar() {
  for (let i = 1; i <= 3; i++) {
    const el = document.getElementById(`vs-${i}`);
    if (!el) continue;
    el.classList.remove('active', 'done');
    if (i < state.step)  el.classList.add('done');
    if (i === state.step) el.classList.add('active');
  }
}


/* ══════════════════════════════════════════
   5. VALIDATION HELPERS
══════════════════════════════════════════ */
function markInvalid(el) {
  el.classList.add('ob-invalid');
  if (window.gsap) gsap.from(el, { x: -5, duration: .18, clearProps: 'x' });
}
function markValid(el) { el.classList.remove('ob-invalid'); }

function validateRadioGroup(name, containerId) {
  const checked = document.querySelector(`input[name="${name}"]:checked`);
  const wrap    = document.getElementById(containerId);
  if (!checked) {
    wrap.style.outline = '2px solid #ef4444';
    wrap.style.outlineOffset = '6px';
    wrap.style.borderRadius = '8px';
    return null;
  }
  wrap.style.outline = '';
  return checked.value;
}


/* ══════════════════════════════════════════
   6. STEP 1 — ABOUT YOU
══════════════════════════════════════════ */
document.getElementById('form-1').addEventListener('submit', e => {
  e.preventDefault();
  let ok = true;

  const reqFields = [
    { id: 'ob-fname',   check: v => v.trim().length >= 1 },
    { id: 'ob-lname',   check: v => v.trim().length >= 1 },
    { id: 'ob-email',   check: v => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v.trim()) },
    { id: 'ob-country', check: v => v !== '' },
  ];
  reqFields.forEach(f => {
    const el = document.getElementById(f.id);
    f.check(el.value) ? markValid(el) : (markInvalid(el), ok = false);
  });

  const stage = validateRadioGroup('stage', 'ob-stage');
  if (!stage) ok = false;

  if (!ok) return;

  state.firstName = document.getElementById('ob-fname').value.trim();
  state.lastName  = document.getElementById('ob-lname').value.trim();
  state.email     = document.getElementById('ob-email').value.trim();
  state.phone     = window.itiInstance ? window.itiInstance.getNumber() : document.getElementById('ob-phone').value.trim();
  state.country   = document.getElementById('ob-country').value;
  state.stage     = stage;

  goToStep(2, 'forward');
  animatePanel2Fields();
});


/* ══════════════════════════════════════════
   7. STEP 2 — COMPANY DETAILS
══════════════════════════════════════════ */

/* Entity type toggle — show/hide Private vs VCC fields */
document.querySelectorAll('input[name="entityType"]').forEach(radio => {
  radio.addEventListener('change', () => {
    const val = radio.value;
    state.entityType = val;
    const privateFields = document.getElementById('fields-private');
    const vccFields     = document.getElementById('fields-vcc');
    privateFields.style.display = val === 'private' ? '' : 'none';
    vccFields.style.display     = val === 'vcc'     ? '' : 'none';
    if (window.lucide) lucide.createIcons();
    // Animate in the newly-shown fields
    if (window.gsap) {
      const target = val === 'vcc' ? vccFields : privateFields;
      gsap.from(target.querySelectorAll('.ob-field, .ob-field-row'), {
        opacity: 0, y: 16, duration: .35, stagger: .05, ease: 'power2.out'
      });
    }
  });
});

function animatePanel2Fields() {
  if (!window.gsap) return;
  const els = document.querySelectorAll('#panel-2 .ob-field, #panel-2 .ob-panel__header, #panel-2 .ob-form__footer');
  gsap.from(els, { opacity: 0, y: 16, duration: .4, stagger: .055, ease: 'power2.out', delay: .1 });
}

document.getElementById('form-2').addEventListener('submit', e => {
  e.preventDefault();
  let ok = true;

  // Validate entity type selection
  const entityType = validateRadioGroup('entityType', 'ob-entity-type');
  if (!entityType) { ok = false; }

  if (entityType === 'private') {
    // ── Private company validation ──
    const reqSelects = ['ob-industry', 'ob-directors', 'ob-shareholders', 'ob-capital', 'ob-fy'];
    reqSelects.forEach(id => {
      const el = document.getElementById(id);
      el.value ? markValid(el) : (markInvalid(el), ok = false);
    });

    const localDir = validateRadioGroup('localDir', 'ob-local-dir');
    const employees = validateRadioGroup('employees', 'ob-employees');
    const timeline  = validateRadioGroup('timeline', 'ob-timeline-group');
    const regAddr   = validateRadioGroup('registeredAddress', 'ob-address-group');
    if (!localDir || !employees || !timeline || !regAddr) ok = false;

    if (!ok) return;

    state.companyName       = document.getElementById('ob-compname').value.trim();
    state.industry          = document.getElementById('ob-industry').value;
    state.bizDesc           = document.getElementById('ob-bizdesc').value.trim();
    state.directors         = document.getElementById('ob-directors').value;
    state.shareholders      = document.getElementById('ob-shareholders').value;
    state.shareCapital      = document.getElementById('ob-capital').value;
    state.fyEnd             = document.getElementById('ob-fy').value;
    state.localDir          = localDir;
    state.employees         = employees;
    state.timeline          = timeline;
    state.registeredAddress = regAddr;

  } else if (entityType === 'vcc') {
    // ── VCC / Fund validation ──
    const reqSelects = ['ob-fund-type', 'ob-fund-strategy', 'ob-fund-aum', 'ob-vcc-directors', 'ob-fund-manager', 'ob-vcc-fy', 'ob-vcc-timeline'];
    reqSelects.forEach(id => {
      const el = document.getElementById(id);
      el.value ? markValid(el) : (markInvalid(el), ok = false);
    });

    const vccAddr = validateRadioGroup('vccRegisteredAddress', 'ob-vcc-address-group');
    if (!vccAddr) ok = false;

    if (!ok) return;

    state.vccName              = document.getElementById('ob-vcc-name').value.trim();
    state.fundType             = document.getElementById('ob-fund-type').value;
    state.fundStrategy         = document.getElementById('ob-fund-strategy').value;
    state.fundAum              = document.getElementById('ob-fund-aum').value;
    state.fundDesc             = document.getElementById('ob-fund-desc').value.trim();
    state.vccDirectors         = document.getElementById('ob-vcc-directors').value;
    state.fundManager          = document.getElementById('ob-fund-manager').value;
    state.vccFyEnd             = document.getElementById('ob-vcc-fy').value;
    state.vccTimeline          = document.getElementById('ob-vcc-timeline').value;
    state.vccRegisteredAddress = vccAddr;

  } else {
    return;
  }

  state.entityType = entityType;
  SERVICES = entityType === 'vcc' ? SERVICES_VCC : SERVICES_PRIVATE;
  state.services.clear();
  buildServicesGrid();
  goToStep(3, 'forward');
});

document.getElementById('back-2').addEventListener('click', () => goToStep(1, 'backward'));


/* ══════════════════════════════════════════
   8. STEP 3 — SERVICES
══════════════════════════════════════════ */
function buildServicesGrid() {
  const grid = document.getElementById('servicesGrid');
  grid.innerHTML = '';
  SERVICES.forEach((svc, i) => {
    const card = document.createElement('div');
    card.className = 'ob-svc-card';
    card.dataset.id = svc.id;
    if (state.services.has(svc.id)) card.classList.add('selected');
    card.innerHTML = `
      <div class="ob-svc-card__check">
        <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="3"><polyline points="20 6 9 17 4 12"/></svg>
      </div>
      <div class="ob-svc-card__icon"><i data-lucide="${svc.icon}"></i></div>
      <div class="ob-svc-card__title">${svc.title}</div>
      <div class="ob-svc-card__desc">${svc.desc}</div>`;
    card.addEventListener('click', () => toggleService(svc.id, card));
    grid.appendChild(card);
    if (window.gsap) gsap.from(card, { y: 18, duration: .38, delay: i * .055, ease: 'power2.out' });
  });
  if (window.lucide) lucide.createIcons();
}

function toggleService(id, card) {
  if (state.services.has(id)) { state.services.delete(id); card.classList.remove('selected'); }
  else {
    state.services.add(id); card.classList.add('selected');
    if (window.gsap) gsap.from(card, { scale: .96, duration: .18, ease: 'back.out(2)' });
  }
  const hasAny = state.services.size > 0;
  document.getElementById('next-3').disabled = !hasAny;
  document.getElementById('servicesNote').classList.toggle('hidden', hasAny);
}

document.getElementById('next-3').addEventListener('click', async () => {
  if (!state.services.size) return;
  const btn = document.getElementById('next-3');
  btn.disabled = true;
  btn.textContent = 'Submitting…';
  await submitOnboarding();
  goToStep(4, 'forward');
  populateSuccess();
  setTimeout(launchConfetti, 500);
});
document.getElementById('back-3').addEventListener('click', () => goToStep(2, 'backward'));


/* ══════════════════════════════════════════
   10. SUBMIT TO CONTACT API
══════════════════════════════════════════ */
async function submitOnboarding() {
  const svcList = Array.from(state.services).map(id => SERVICES.find(s => s.id === id)?.title).filter(Boolean).join(', ');

  const payload = {
    name:       `${state.firstName} ${state.lastName}`,
    email:      state.email,
    phone:      state.phone || '',
    service:    svcList,
    source:     'onboarding',
    entityType: state.entityType,
    stage:      state.stage,
    country:    state.country,
  };

  if (state.entityType === 'vcc') {
    payload.vcc = {
      name:              state.vccName || '',
      fundType:          state.fundType,
      strategy:          state.fundStrategy,
      aum:               state.fundAum,
      description:       state.fundDesc || '',
      directors:         state.vccDirectors,
      fundManager:       state.fundManager,
      fyEnd:             state.vccFyEnd,
      timeline:          state.vccTimeline,
      registeredAddress: state.vccRegisteredAddress,
    };
  } else {
    payload.company = {
      name:              state.companyName || '',
      industry:          state.industry,
      description:       state.bizDesc || '',
      directors:         state.directors,
      shareholders:      state.shareholders,
      shareCapital:      state.shareCapital,
      fyEnd:             state.fyEnd,
      localDirector:     state.localDir,
      employees:         state.employees,
      timeline:          state.timeline,
      registeredAddress: state.registeredAddress,
    };
  }

  try {
    await fetch('/api/contact', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
  } catch (_) { /* silent */ }
}


/* ══════════════════════════════════════════
   11. SUCCESS SCREEN
══════════════════════════════════════════ */
function populateSuccess() {
  document.getElementById('successName').textContent = state.firstName;

  const svcList = Array.from(state.services)
    .map(id => SERVICES.find(s => s.id === id)?.title)
    .filter(Boolean).join(' · ');

  const STAGE_LABELS = { new: 'Starting fresh', existing: 'Already incorporated', foreign: 'Foreign expansion' };
  const DIR_LABELS   = { yes: 'Yes, I have one', no: 'No — needs nominee', unsure: 'Not sure yet' };
  const EMP_LABELS   = { 'yes-immediate': 'Yes, immediately', 'yes-later': 'Yes, later', no: 'No' };
  const TL_LABELS    = { asap: 'ASAP', '1 month': '~1 month', '1-3 months': '1–3 months', '3+ months': '3+ months', exploring: 'Just exploring' };
  const FUND_MGR_LABELS = { 'yes-licensed': 'Yes, MAS-licensed', 'yes-exempt': 'Yes, exempt (RFMC/A-CIS)', no: 'No — need one appointed', 'not sure': 'Not sure' };

  let summaryRows = `
    <h4>Your enquiry summary</h4>
    <div class="ob-success__row"><strong>Name</strong><span>${state.firstName} ${state.lastName}</span></div>
    <div class="ob-success__row"><strong>Email</strong><span>${state.email}</span></div>
    ${state.phone ? `<div class="ob-success__row"><strong>Phone</strong><span>${state.phone}</span></div>` : ''}
    <div class="ob-success__row"><strong>Entity type</strong><span>${state.entityType === 'vcc' ? 'VCC / Fund' : 'Private Company (Pte. Ltd.)'}</span></div>
    <div class="ob-success__row"><strong>Stage</strong><span>${STAGE_LABELS[state.stage] || state.stage}</span></div>`;

  if (state.entityType === 'vcc') {
    summaryRows += `
    ${state.vccName ? `<div class="ob-success__row"><strong>VCC name</strong><span>${state.vccName}</span></div>` : ''}
    <div class="ob-success__row"><strong>Fund type</strong><span>${state.fundType}</span></div>
    <div class="ob-success__row"><strong>Strategy</strong><span>${state.fundStrategy}</span></div>
    <div class="ob-success__row"><strong>Expected AUM</strong><span>${state.fundAum}</span></div>
    <div class="ob-success__row"><strong>Directors</strong><span>${state.vccDirectors}</span></div>
    <div class="ob-success__row"><strong>Fund manager</strong><span>${FUND_MGR_LABELS[state.fundManager] || state.fundManager}</span></div>
    <div class="ob-success__row"><strong>FY end</strong><span>${state.vccFyEnd}</span></div>
    <div class="ob-success__row"><strong>Timeline</strong><span>${TL_LABELS[state.vccTimeline] || state.vccTimeline}</span></div>`;
  } else {
    summaryRows += `
    ${state.companyName ? `<div class="ob-success__row"><strong>Company</strong><span>${state.companyName}</span></div>` : ''}
    <div class="ob-success__row"><strong>Industry</strong><span>${state.industry}</span></div>
    <div class="ob-success__row"><strong>Directors</strong><span>${state.directors}</span></div>
    <div class="ob-success__row"><strong>Shareholders</strong><span>${state.shareholders}</span></div>
    <div class="ob-success__row"><strong>Share capital</strong><span>${state.shareCapital}</span></div>
    <div class="ob-success__row"><strong>FY end</strong><span>${state.fyEnd}</span></div>
    <div class="ob-success__row"><strong>Local director</strong><span>${DIR_LABELS[state.localDir] || state.localDir}</span></div>
    <div class="ob-success__row"><strong>Employees</strong><span>${EMP_LABELS[state.employees] || state.employees}</span></div>
    <div class="ob-success__row"><strong>Timeline</strong><span>${TL_LABELS[state.timeline] || state.timeline}</span></div>`;
  }

  summaryRows += `
    <div class="ob-success__row"><strong>Services</strong><span>${svcList || '—'}</span></div>`;

  document.getElementById('successSummary').innerHTML = summaryRows;

  if (window.gsap) {
    gsap.from('#panel-4 .ob-success__ring',    { scale: 0, duration: .55, ease: 'back.out(2)', delay: .1 });
    gsap.from('#panel-4 .ob-success__title',   { opacity: 0, y: 16, duration: .4, delay: .35 });
    gsap.from('#panel-4 .ob-success__sub',     { opacity: 0, y: 16, duration: .4, delay: .45 });
    gsap.from('#panel-4 .ob-success__summary', { opacity: 0, y: 16, duration: .4, delay: .55 });
    gsap.from('#panel-4 .ob-success__actions', { opacity: 0, y: 16, duration: .4, delay: .65 });
  }
  setTimeout(() => document.getElementById('successRing')?.classList.add('pulse'), 700);
}


/* ══════════════════════════════════════════
   12. CONFETTI
══════════════════════════════════════════ */
function launchConfetti() {
  const canvas = document.getElementById('confettiCanvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  canvas.width = window.innerWidth; canvas.height = window.innerHeight;
  const COLORS = ['#1A6BCC','#00C9A7','#FF5C35','#F5A623','#fff','#163758'];
  const pieces = Array.from({ length: 130 }, () => ({
    x: Math.random() * canvas.width, y: -10 - Math.random() * canvas.height * .35,
    w: Math.random() * 10 + 4, h: Math.random() * 6 + 3,
    r: Math.random() * Math.PI * 2, vx: (Math.random() - .5) * 3,
    vy: Math.random() * 4 + 2, vr: (Math.random() - .5) * .2,
    c: COLORS[Math.floor(Math.random() * COLORS.length)], alpha: 1,
  }));
  let frame = 0;
  function tick() {
    ctx.clearRect(0, 0, canvas.width, canvas.height); frame++;
    let alive = false;
    pieces.forEach(p => {
      p.x += p.vx; p.y += p.vy; p.r += p.vr; p.vy += .08;
      if (frame > 120) p.alpha -= .015;
      if (p.alpha <= 0) return;
      alive = true;
      ctx.save(); ctx.globalAlpha = Math.max(0, p.alpha);
      ctx.translate(p.x, p.y); ctx.rotate(p.r);
      ctx.fillStyle = p.c; ctx.fillRect(-p.w / 2, -p.h / 2, p.w, p.h);
      ctx.restore();
    });
    if (alive) requestAnimationFrame(tick);
    else ctx.clearRect(0, 0, canvas.width, canvas.height);
  }
  requestAnimationFrame(tick);
}


/* ══════════════════════════════════════════
   13. INIT
══════════════════════════════════════════ */
(function init() {
  /* intl-tel-input */
  const phoneInput = document.getElementById('ob-phone');
  if (phoneInput && window.intlTelInput) {
    window.itiInstance = intlTelInput(phoneInput, {
      initialCountry: 'sg',
      preferredCountries: ['sg', 'my', 'in', 'cn', 'gb', 'us', 'au', 'hk'],
      separateDialCode: true,
      dropdownContainer: document.body,
      utilsScript: 'https://cdn.jsdelivr.net/npm/intl-tel-input@25.3.1/build/js/utils.js',
    });
  }

  updateProgress();
  updateSidebar();
  if (window.lucide) lucide.createIcons();
  if (window.gsap) {
    const els = '#panel-1 .ob-field, #panel-1 .ob-radio-group, #panel-1 .ob-panel__header, #panel-1 .ob-form__footer';
    gsap.from(document.querySelectorAll(els), { opacity: 0, y: 20, duration: .5, stagger: .07, ease: 'power2.out', delay: .15 });
    gsap.from('.ob-topbar', { opacity: 0, y: -10, duration: .4, ease: 'power2.out' });
    gsap.from('.ob-left__inner > *', { opacity: 0, y: 24, duration: .5, stagger: .1, ease: 'power2.out', delay: .1 });
  }
})();
