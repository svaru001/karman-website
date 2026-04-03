/* ─────────────────────────────────────────────
   KARMAN — Interactive Tools Engine
   tools.js
───────────────────────────────────────────── */

/* ══════════════════════════════════════════
   TOOL DEFINITIONS
══════════════════════════════════════════ */

const TOOLS = {

  /* ─── 1. BUSINESS STRUCTURE RECOMMENDER ─── */
  businessStructure: {
    tag: 'Business Structure Recommender',
    title: 'Find the right structure for your business',
    totalSteps: 7,
    steps: [
      {
        type: 'question',
        question: 'Are you setting up the business alone or with partners?',
        sub: 'This helps us understand the ownership structure.',
        options: [
          { emoji: '🙋', label: 'Just me', desc: 'Sole founder, single owner', value: 'sole' },
          { emoji: '🤝', label: '2–5 partners', desc: 'Small group of co-founders', value: 'small' },
          { emoji: '🏢', label: '6+ shareholders', desc: 'Larger group or investors', value: 'large' }
        ]
      },
      {
        type: 'question',
        question: 'What is your residency status?',
        sub: 'Singapore residency affects the incorporation requirements.',
        options: [
          { emoji: '🇸🇬', label: 'Singapore Citizen or PR', desc: 'Local resident', value: 'local' },
          { emoji: '✈️', label: 'Employment Pass Holder', desc: 'Working in Singapore', value: 'ep' },
          { emoji: '🌏', label: 'Based overseas', desc: 'Foreign founder, not in Singapore', value: 'foreign' }
        ]
      },
      {
        type: 'question',
        question: 'Do you want personal liability protection?',
        sub: 'Limited liability means your personal assets are protected if the business has debts.',
        options: [
          { emoji: '🛡️', label: 'Yes, protect my assets', desc: 'I want a legal separation between me and the business', value: 'yes' },
          { emoji: '🤷', label: 'Not a priority right now', desc: 'I\'m starting small and keeping things simple', value: 'no' }
        ]
      },
      {
        type: 'question',
        question: 'Do you plan to raise funding or take on investors?',
        sub: 'Some structures are far easier to raise capital with than others.',
        options: [
          { emoji: '🚀', label: 'Yes, I plan to fundraise', desc: 'I want to be investment-ready', value: 'yes' },
          { emoji: '💼', label: 'No, self-funded for now', desc: 'Bootstrapping or using revenue', value: 'no' }
        ]
      },
      {
        type: 'question',
        question: 'How would you describe your growth ambitions?',
        options: [
          { emoji: '📈', label: 'Significant growth', desc: 'I plan to hire, scale, and expand', value: 'high' },
          { emoji: '🌱', label: 'Steady lifestyle business', desc: 'Comfortable, sustainable income', value: 'low' }
        ]
      },
      {
        type: 'question',
        question: 'Is corporate tax efficiency important to you?',
        sub: 'Singapore Pte Ltd companies enjoy attractive tax rates and startup exemptions.',
        options: [
          { emoji: '💰', label: 'Yes, I want to optimise tax', desc: 'Efficient structure matters to me', value: 'yes' },
          { emoji: '😊', label: 'Not my main concern', desc: 'I\'ll worry about this later', value: 'no' }
        ]
      },
      {
        type: 'capture',
        heading: 'Get your personalised recommendation',
        sub: 'Enter your details below and we\'ll send your tailored business structure recommendation, including pros, cons, and setup costs.',
        ctaText: 'Send my recommendation →'
      }
    ],
    getResult(answers) {
      const ownership = answers[0];
      const liability = answers[2];
      const funding   = answers[3];
      const growth    = answers[4];
      const residency = answers[1];

      if (funding === 'yes' || liability === 'yes' || growth === 'high' || ownership === 'large' || residency === 'foreign') {
        return {
          structure: 'Private Limited Company (Pte Ltd)',
          icon: '🏢',
          badge: 'Recommended',
          badgeType: 'teal',
          desc: 'A Singapore Private Limited Company (Pte Ltd) is the gold standard for businesses with growth ambitions. It offers limited liability protection, tax advantages, and the credibility needed to attract customers, partners, and investors.',
          features: [
            'Full personal liability protection',
            'Corporate tax rate of 17% (with startup exemptions for first 3 years)',
            'Ability to issue shares and raise funding',
            'Perpetual existence — separate legal entity',
            'Professional image with "Pte Ltd" designation'
          ]
        };
      }
      if (ownership === 'small') {
        return {
          structure: 'General Partnership or LLP',
          icon: '🤝',
          badge: 'Good Fit',
          badgeType: 'blue',
          desc: 'A Limited Liability Partnership (LLP) suits small groups of partners who want some liability protection with lower compliance requirements. However, for most growing businesses, a Pte Ltd remains the better long-term choice.',
          features: [
            'Shared ownership between partners',
            'Lower compliance costs than Pte Ltd',
            'Partners taxed at personal income tax rates',
            'LLP provides some liability protection'
          ]
        };
      }
      return {
        structure: 'Sole Proprietorship',
        icon: '🙋',
        badge: 'Simple Start',
        badgeType: 'blue',
        desc: 'A Sole Proprietorship is the simplest and cheapest structure to register in Singapore. It\'s suitable for testing an idea or freelancing, but note there is no liability protection — you are personally liable for business debts.',
        features: [
          'Lowest setup and maintenance costs',
          'Simplest compliance requirements',
          'Income taxed at personal rate',
          'No personal liability protection',
          'Easy to upgrade to Pte Ltd later'
        ]
      };
    }
  },

  /* ─── 2. COST CALCULATOR ─── */
  costCalculator: {
    tag: 'Cost Calculator',
    title: 'Estimate your annual service fees',
    totalSteps: 4,
    steps: [
      {
        type: 'calc-services',
        question: 'Which services do you need?',
        sub: 'Select all that apply — you can always add more later.',
        services: [
          { id: 'incorporation', icon: '🏢', label: 'Company Incorporation' },
          { id: 'secretary', icon: '📋', label: 'Corporate Secretary' },
          { id: 'accounting', icon: '📊', label: 'Accounting & Bookkeeping' },
          { id: 'tax', icon: '🧾', label: 'Corporate Tax Filing' },
          { id: 'gst', icon: '📑', label: 'GST Registration & Filing' },
          { id: 'payroll', icon: '👥', label: 'Payroll Services' }
        ]
      },
      {
        type: 'calc-sliders',
        question: 'Tell us a bit more about your company',
        sub: 'This helps us give you an accurate estimate.',
      },
      {
        type: 'calc-estimate',
        question: 'Your estimated annual fees'
      },
      {
        type: 'capture',
        heading: 'Get your detailed quote',
        sub: 'Leave your details and one of our advisors will prepare a precise, itemised quote within 1 business day.',
        ctaText: 'Request my quote →',
        extraFields: '<div class="form-group"><label for="tool-phone">Phone (optional)</label><input type="tel" id="tool-phone" placeholder="+65 9123 4567" autocomplete="tel" /></div>'
      }
    ]
  },

  /* ─── 3. ELIGIBILITY CHECKER ─── */
  eligibilityChecker: {
    tag: 'Eligibility Checker',
    title: 'Check your eligibility to register in Singapore',
    totalSteps: 8,
    steps: [
      {
        type: 'question',
        question: 'Are you 18 years of age or older?',
        options: [
          { emoji: '✅', label: 'Yes', value: 'yes', next: 1 },
          { emoji: '❌', label: 'No', value: 'no', next: 'disqualified' }
        ]
      },
      {
        type: 'question',
        question: 'Is your proposed business activity legal in Singapore?',
        sub: 'Certain activities (e.g. gambling, unlicensed money lending) are prohibited.',
        options: [
          { emoji: '✅', label: 'Yes, it\'s legal', value: 'yes', next: 2 },
          { emoji: '❌', label: 'No / Not sure', value: 'no', next: 'disqualified' }
        ]
      },
      {
        type: 'question',
        question: 'Do you have at least one director who is ordinarily resident in Singapore?',
        sub: 'Under the Companies Act, every company must have at least one locally-resident director.',
        options: [
          { emoji: '✅', label: 'Yes', value: 'yes', next: 3 },
          { emoji: '🌏', label: 'No — I\'m a foreign founder', value: 'no', next: 3 }
        ]
      },
      {
        type: 'question',
        question: 'Have you identified at least one shareholder?',
        sub: 'A Singapore Pte Ltd can have 1 to 50 shareholders.',
        options: [
          { emoji: '✅', label: 'Yes', value: 'yes', next: 4 },
          { emoji: '🤔', label: 'Not yet', value: 'no', next: 4 }
        ]
      },
      {
        type: 'question',
        question: 'Does your business involve any regulated activities?',
        sub: 'E.g. financial services, healthcare, education, food & beverage, employment agency.',
        options: [
          { emoji: '⚠️', label: 'Yes', value: 'yes', next: 5 },
          { emoji: '✅', label: 'No', value: 'no', next: 5 }
        ]
      },
      {
        type: 'question',
        question: 'Have you chosen a company name?',
        sub: 'The name must be available on ACRA\'s register and not infringe any trademarks.',
        options: [
          { emoji: '✅', label: 'Yes, I have a name ready', value: 'yes', next: 6 },
          { emoji: '💭', label: 'Still deciding', value: 'no', next: 6 }
        ]
      },
      {
        type: 'question',
        question: 'Do you have your identification documents ready?',
        sub: 'Passport or NRIC for all directors and shareholders.',
        options: [
          { emoji: '✅', label: 'Yes, all ready', value: 'yes', next: 7 },
          { emoji: '📋', label: 'Not yet — I need a checklist', value: 'no', next: 7 }
        ]
      },
      {
        type: 'eligibility-result'
      }
    ]
  },

  /* ─── 4. TIMELINE VISUALIZER ─── */
  timelineVisualizer: {
    tag: 'Incorporation Timeline',
    title: 'Your journey from idea to registered company',
    totalSteps: 2,
    steps: [
      {
        type: 'timeline',
        items: [
          { emoji: '💬', timing: 'Day 0', title: 'Free Consultation', desc: 'Discuss your needs, choose your structure, and confirm fees. No obligation.' },
          { emoji: '📋', timing: 'Day 1', title: 'Document Collection & Preparation', desc: 'We collect your KYC documents and prepare all required ACRA forms and your company constitution.' },
          { emoji: '📤', timing: 'Day 1–2', title: 'ACRA Submission', desc: 'We submit your incorporation application electronically as a registered filing agent.' },
          { emoji: '🎉', timing: 'Day 2–4', title: 'ACRA Approval & UEN Issued', desc: 'Your company is legally incorporated. You receive your Unique Entity Number (UEN).' },
          { emoji: '📦', timing: 'Day 3–5', title: 'Post-Incorporation Documents', desc: 'Share certificates, board resolutions, register of directors, and CorpPass setup.' },
          { emoji: '🏦', timing: 'Day 5–14', title: 'Business Bank Account', desc: 'Open a business account with DBS, OCBC, UOB or another Singapore bank using your UEN.' },
          { emoji: '🚀', timing: 'Day 14+', title: 'You\'re Open for Business', desc: 'Start trading, issuing invoices, hiring staff, and growing your Singapore company.' }
        ]
      },
      {
        type: 'capture',
        heading: 'Ready to start your incorporation?',
        sub: 'Enter your details and our team will reach out to kick off the process — most companies are incorporated within 48 hours.',
        ctaText: 'Start my incorporation →'
      }
    ]
  },

  /* ─── 5. DOCUMENT CHECKLIST ─── */
  documentChecklist: {
    tag: 'Document Checklist',
    title: 'Documents you\'ll need for incorporation',
    totalSteps: 2,
    steps: [
      {
        type: 'checklist',
        categories: [
          {
            title: 'For All Directors & Shareholders',
            items: [
              { id: 'doc1', text: 'Valid passport (foreigners) or NRIC (Singapore citizens/PRs)' },
              { id: 'doc2', text: 'Proof of residential address (utility bill or bank statement, less than 3 months old)' },
              { id: 'doc3', text: 'Personal particulars: full legal name, ID number, nationality, date of birth' },
              { id: 'doc4', text: 'Contact details: email address and mobile number' }
            ]
          },
          {
            title: 'For the Company',
            items: [
              { id: 'doc5', text: 'Proposed company name (have 1–2 alternatives ready in case it\'s taken)' },
              { id: 'doc6', text: 'Proposed business activity description (SSIC code — we can help you find this)' },
              { id: 'doc7', text: 'Registered office address in Singapore (we can provide this)' },
              { id: 'doc8', text: 'Share structure: number of shares and percentage each shareholder will hold' },
              { id: 'doc9', text: 'Paid-up capital amount (minimum S$1, typically S$1–S$100 for a startup)' }
            ]
          },
          {
            title: 'For Foreign Founders Only',
            items: [
              { id: 'doc10', text: 'Certified true copy of passport (notarised or apostilled)' },
              { id: 'doc11', text: 'Nominee director arrangement (we can provide this service)' },
              { id: 'doc12', text: 'Notarised proof of overseas address' }
            ]
          },
          {
            title: 'After Incorporation (prepare these next)',
            items: [
              { id: 'doc13', text: 'Open a business bank account using your new UEN' },
              { id: 'doc14', text: 'Set up CorpPass for government digital services' },
              { id: 'doc15', text: 'Register for GST if your annual turnover exceeds S$1 million' },
              { id: 'doc16', text: 'Appoint a corporate secretary within 6 months of incorporation' }
            ]
          }
        ]
      },
      {
        type: 'capture',
        heading: 'Download your personalised checklist',
        sub: 'Enter your email and we\'ll send you a PDF version of this checklist, plus a step-by-step guide to get started.',
        ctaText: 'Send me the checklist →'
      }
    ]
  }
};

/* ══════════════════════════════════════════
   MODAL ENGINE
══════════════════════════════════════════ */

// ── Mode detection: 'inline' on tool pages, 'modal' on homepage ──
const INLINE_ROOT = document.getElementById('toolInlineRoot');
const MODE = INLINE_ROOT ? 'inline' : 'modal';

const modal   = MODE === 'modal' ? document.getElementById('toolModal')        : null;
const body    = MODE === 'modal' ? document.getElementById('toolModalBody')    : document.getElementById('toolInlineBody');
const title   = MODE === 'modal' ? document.getElementById('toolModalTitle')   : document.getElementById('toolInlineTitle');
const tag     = MODE === 'modal' ? document.getElementById('toolModalTag')     : document.getElementById('toolInlineTag');
const bar     = MODE === 'modal' ? document.getElementById('toolProgressBar')  : document.getElementById('toolInlineBar');
const label   = MODE === 'modal' ? document.getElementById('toolStepLabel')    : document.getElementById('toolInlineLabel');
const nextBtn = MODE === 'modal' ? document.getElementById('toolNextBtn')      : document.getElementById('toolInlineNextBtn');
const backBtn = MODE === 'modal' ? document.getElementById('toolBackBtn')      : document.getElementById('toolInlineBackBtn');

let state = {
  toolId: null,
  step: 0,
  history: [],
  answers: {},
  triggerEl: null
};

// ── Open ──
function openTool(toolId, triggerEl) {
  const tool = TOOLS[toolId];
  if (!tool) return;
  state = { toolId, step: 0, history: [], answers: {}, triggerEl };

  tag.textContent = tool.tag;
  title.textContent = tool.title;
  modal.classList.add('tool-modal--open');
  lockScroll();
  renderStep();
  trapFocus();
}

// ── Close ──
function closeTool() {
  modal.classList.remove('tool-modal--open');
  unlockScroll();
  if (state.triggerEl) state.triggerEl.focus();
  state = { toolId: null, step: 0, history: [], answers: {}, triggerEl: null };
}

// ── Advance ──
function advance() {
  const tool = TOOLS[state.toolId];
  const step = tool.steps[state.step];

  // Validate before advancing
  if (step.type === 'question') {
    const selected = body.querySelector('.wizard-option.selected');
    if (!selected) { showToolError('Please select an option to continue.'); return; }
    const value = selected.dataset.value;
    state.answers[state.step] = value;

    // Branching support
    const opt = step.options.find(o => o.value === value);
    const nextStep = opt && opt.next !== undefined ? opt.next : state.step + 1;
    state.history.push(state.step);
    if (nextStep === 'disqualified') {
      goToDisqualified();
      return;
    }
    state.step = nextStep;
    renderStep();
    return;
  }

  if (step.type === 'calc-services') {
    const selected = [...body.querySelectorAll('.calc-service.selected')].map(el => el.dataset.service);
    if (selected.length === 0) { showToolError('Please select at least one service.'); return; }
    state.answers[state.step] = selected;
    state.history.push(state.step);
    state.step++;
    renderStep();
    return;
  }

  if (step.type === 'calc-sliders') {
    const revenue = body.querySelector('#revenueSlider');
    const employees = body.querySelector('#employeeSlider');
    state.answers.revenue = revenue ? parseInt(revenue.value) : 0;
    state.answers.employees = employees ? parseInt(employees.value) : 0;
    state.history.push(state.step);
    state.step++;
    renderStep();
    return;
  }

  if (step.type === 'eligibility-result' || step.type === 'calc-estimate' || step.type === 'timeline' || step.type === 'checklist') {
    state.history.push(state.step);
    state.step++;
    renderStep();
    return;
  }

  if (step.type === 'capture') {
    const nameEl  = body.querySelector('#tool-name');
    const emailEl = body.querySelector('#tool-email');
    if (!nameEl.value.trim())  { showToolError('Please enter your name.'); nameEl.focus(); return; }
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(emailEl.value)) { showToolError('Please enter a valid email address.'); emailEl.focus(); return; }
    state.answers.name  = nameEl.value.trim();
    state.answers.email = emailEl.value.trim();
    simulateSubmit();
    return;
  }
}

// ── Back ──
function goBack() {
  if (state.history.length === 0) return;
  state.step = state.history.pop();
  renderStep();
}

// ── Go to disqualified result ──
function goToDisqualified() {
  renderDisqualified();
  nextBtn.textContent = 'Book a free consultation →';
  nextBtn.onclick = () => { closeTool(); document.querySelector('#contact').scrollIntoView({ behavior: 'smooth' }); };
  backBtn.classList.remove('visible');
  updateProgress(100, 'Complete');
}

/* ══════════════════════════════════════════
   STEP RENDERERS
══════════════════════════════════════════ */

function renderStep() {
  const tool = TOOLS[state.toolId];
  const step = tool.steps[state.step];

  clearError();
  updateProgress(
    Math.round(((state.step) / (tool.totalSteps)) * 100),
    `Step ${Math.min(state.step + 1, tool.totalSteps)} of ${tool.totalSteps}`
  );
  backBtn.className = 'btn btn--ghost tool-modal__back' + (state.history.length > 0 ? ' visible' : '');
  nextBtn.textContent = 'Continue →';
  nextBtn.onclick = advance;

  switch (step.type) {
    case 'question':        renderQuestion(step); break;
    case 'calc-services':   renderCalcServices(step); break;
    case 'calc-sliders':    renderCalcSliders(step); break;
    case 'calc-estimate':   renderCalcEstimate(step); break;
    case 'eligibility-result': renderEligibilityResult(); break;
    case 'timeline':        renderTimeline(step); break;
    case 'checklist':       renderChecklist(step); break;
    case 'capture':         renderCapture(step); break;
    default: body.innerHTML = '';
  }

  body.scrollTop = 0;
  trapFocus();
}

// ── Question ──
function renderQuestion(step) {
  const savedValue = state.answers[state.step];
  const gridClass  = step.options.length > 3 ? 'wizard-options--grid' : '';

  body.innerHTML = `
    <div class="wizard-question">
      <p class="wizard-question__text">${step.question}</p>
      ${step.sub ? `<p class="wizard-question__sub">${step.sub}</p>` : ''}
      <div class="wizard-options ${gridClass}">
        ${step.options.map(opt => `
          <button class="wizard-option ${savedValue === opt.value ? 'selected' : ''}" data-value="${opt.value}" type="button">
            <span class="wizard-option__emoji">${opt.emoji}</span>
            <div>
              <span class="wizard-option__label">${opt.label}</span>
              ${opt.desc ? `<span class="wizard-option__desc">${opt.desc}</span>` : ''}
            </div>
          </button>
        `).join('')}
      </div>
    </div>`;

  body.querySelectorAll('.wizard-option').forEach(btn => {
    btn.addEventListener('click', () => {
      body.querySelectorAll('.wizard-option').forEach(b => b.classList.remove('selected'));
      btn.classList.add('selected');
      clearError();
    });
  });
}

// ── Calc: Services ──
function renderCalcServices(step) {
  const saved = state.answers[state.step] || [];
  body.innerHTML = `
    <p class="wizard-question__text">${step.question}</p>
    <p class="wizard-question__sub">${step.sub}</p>
    <div class="calc-services">
      ${step.services.map(s => `
        <button class="calc-service ${saved.includes(s.id) ? 'selected' : ''}" data-service="${s.id}" type="button">
          <span class="calc-service__check"></span>
          <span class="calc-service__icon">${s.icon}</span>
          <span class="calc-service__label">${s.label}</span>
        </button>
      `).join('')}
    </div>`;

  body.querySelectorAll('.calc-service').forEach(btn => {
    btn.addEventListener('click', () => {
      btn.classList.toggle('selected');
      clearError();
    });
  });
}

// ── Calc: Sliders ──
function renderCalcSliders(step) {
  const services  = state.answers[0] || [];
  const needsRev  = services.some(s => ['accounting', 'tax'].includes(s));
  const needsPay  = services.includes('payroll');
  const revVal    = state.answers.revenue   || 150000;
  const payVal    = state.answers.employees || 5;

  body.innerHTML = `
    <p class="wizard-question__text">${step.question}</p>
    <p class="wizard-question__sub">${step.sub}</p>
    ${needsRev ? `
    <div class="calc-slider-wrap">
      <div class="calc-slider-label">
        <span>Annual Revenue</span>
        <strong id="revLabel">S$${formatNum(revVal)}</strong>
      </div>
      <input type="range" class="calc-slider" id="revenueSlider"
        min="50000" max="1000000" step="50000" value="${revVal}" />
    </div>` : ''}
    ${needsPay ? `
    <div class="calc-slider-wrap">
      <div class="calc-slider-label">
        <span>Number of Employees</span>
        <strong id="payLabel">${payVal}</strong>
      </div>
      <input type="range" class="calc-slider" id="employeeSlider"
        min="1" max="50" step="1" value="${payVal}" />
    </div>` : ''}
    ${!needsRev && !needsPay ? '<p style="color:var(--gray-600);font-size:14px;padding:12px 0;">No additional details needed for your selected services.</p>' : ''}
  `;

  const revSlider = body.querySelector('#revenueSlider');
  const paySlider = body.querySelector('#employeeSlider');
  if (revSlider) {
    revSlider.addEventListener('input', () => {
      document.getElementById('revLabel').textContent = 'S$' + formatNum(revSlider.value);
      updateSliderFill(revSlider);
    });
    updateSliderFill(revSlider);
  }
  if (paySlider) {
    paySlider.addEventListener('input', () => {
      document.getElementById('payLabel').textContent = paySlider.value;
      updateSliderFill(paySlider);
    });
    updateSliderFill(paySlider);
  }
}

// ── Calc: Estimate ──
function renderCalcEstimate(step) {
  const services  = state.answers[0] || [];
  const revenue   = state.answers.revenue   || 150000;
  const employees = state.answers.employees || 5;
  const breakdown = [];
  let totalMin = 0, totalMax = 0;

  const pricing = {
    incorporation: { label: 'Company Incorporation', min: 699,  max: 2800 },
    secretary:     { label: 'Corporate Secretary',   min: 350,  max: 1500 },
    tax:           { label: 'Corporate Tax Filing',  min: 300,  max: 600  },
    gst:           { label: 'GST Registration & Filing', min: 400, max: 700 }
  };

  services.forEach(s => {
    if (pricing[s]) {
      breakdown.push({ label: pricing[s].label, min: pricing[s].min, max: pricing[s].max });
      totalMin += pricing[s].min; totalMax += pricing[s].max;
    }
    if (s === 'accounting') {
      let mn, mx;
      if (revenue <= 150000)      { mn = 900;  mx = 1200; }
      else if (revenue <= 500000) { mn = 1800; mx = 2400; }
      else                        { mn = 3600; mx = 4800; }
      breakdown.push({ label: 'Accounting & Bookkeeping', min: mn, max: mx });
      totalMin += mn; totalMax += mx;
    }
    if (s === 'payroll') {
      const mn = employees * 300, mx = employees * 500;
      breakdown.push({ label: `Payroll (${employees} employee${employees > 1 ? 's' : ''})`, min: mn, max: mx });
      totalMin += mn; totalMax += mx;
    }
  });

  body.innerHTML = `
    <div class="estimate-card">
      <div class="estimate-card__label">Estimated Annual Fee</div>
      <div class="estimate-card__amount">S$${formatNum(totalMin)} – S$${formatNum(totalMax)}</div>
      <div class="estimate-card__note">Based on your selections. Exact pricing confirmed after consultation.</div>
      <div class="estimate-breakdown">
        ${breakdown.map(b => `
          <div class="estimate-breakdown__item">
            <span>${b.label}</span>
            <strong>S$${formatNum(b.min)}–S$${formatNum(b.max)}</strong>
          </div>`).join('')}
      </div>
    </div>
    <p style="font-size:13px;color:var(--gray-600);text-align:center;">All prices exclude GST. Government fees included.</p>
  `;

  nextBtn.textContent = 'Get detailed quote →';
}

// ── Eligibility Result ──
function renderEligibilityResult() {
  const answers = state.answers;
  const hasNoDirector = answers[2] === 'no';
  const hasRegulated  = answers[4] === 'yes';
  const missingDocs   = answers[6] === 'no';
  const missingName   = answers[5] === 'no';

  let html = '';
  if (Object.values(answers).some(v => v === 'no' && [0,1].includes(parseInt(Object.keys(answers).find(k => answers[k] === v))))) {
    renderDisqualified(); return;
  }

  const notes = [];
  if (hasNoDirector) notes.push('You\'ll need a nominee director — we can provide this service.');
  if (hasRegulated)  notes.push('Your business activity may require additional licences from MAS, MOH, or another authority.');
  if (missingDocs)   notes.push('Use our Document Checklist tool to track which documents you still need.');
  if (missingName)   notes.push('We can help you check name availability on ACRA before submitting.');

  const type = notes.length > 0 ? 'conditional' : 'eligible';
  html = `
    <div class="eligibility-result eligibility-result--${type}">
      <div class="eligibility-result__icon">${type === 'eligible' ? '🎉' : '⚠️'}</div>
      <div class="eligibility-result__title">${type === 'eligible' ? 'You\'re eligible to incorporate!' : 'You\'re eligible — with a few things to sort'}</div>
      <p>${type === 'eligible'
        ? 'Great news! Based on your answers, you meet the basic requirements to register a Singapore Pte Ltd. Our team can get you incorporated in as little as 48 hours.'
        : 'You can still incorporate — there are just a few things to take care of first. Our team can guide you through each one.'
      }</p>
      ${notes.length > 0 ? `<div class="eligibility-notes">${notes.map(n => `<div class="eligibility-note"><span class="eligibility-note__dot"></span>${n}</div>`).join('')}</div>` : ''}
    </div>
  `;
  body.innerHTML = html;
  nextBtn.textContent = 'Book a free consultation →';
  nextBtn.onclick = () => {
    state.history.push(state.step);
    state.step++;
    renderStep();
  };
  updateProgress(100, 'Complete');
  backBtn.classList.add('visible');
}

function renderDisqualified() {
  body.innerHTML = `
    <div class="eligibility-result eligibility-result--ineligible">
      <div class="eligibility-result__icon">🚫</div>
      <div class="eligibility-result__title">Not eligible right now</div>
      <p>Based on your answers, you don't currently meet the requirements to register a Singapore company. This may be due to age restrictions or the nature of your proposed business activity.</p>
      <div class="eligibility-notes">
        <div class="eligibility-note"><span class="eligibility-note__dot" style="background:var(--gray-400)"></span>Directors must be at least 18 years old.</div>
        <div class="eligibility-note"><span class="eligibility-note__dot" style="background:var(--gray-400)"></span>All business activities must comply with Singapore law.</div>
      </div>
    </div>
    <p style="font-size:14px;color:var(--gray-600);margin-top:16px;line-height:1.65;">If you think this result is incorrect or want to discuss your specific situation, our advisors are happy to help — no obligation.</p>
  `;
}

// ── Timeline ──
function renderTimeline(step) {
  body.innerHTML = `
    <div class="timeline">
      ${step.items.map((item, i) => `
        <div class="timeline-step" data-index="${i}">
          <div class="timeline-step__node">${item.emoji}</div>
          <div class="timeline-step__content">
            <div class="timeline-step__timing">${item.timing}</div>
            <div class="timeline-step__title">${item.title}</div>
            <div class="timeline-step__desc">${item.desc}</div>
          </div>
        </div>
      `).join('')}
    </div>`;

  nextBtn.textContent = 'Start my incorporation →';
  updateProgress(50, 'Step 1 of 2');

  const steps = body.querySelectorAll('.timeline-step');
  steps.forEach((el, i) => {
    setTimeout(() => el.classList.add('visible'), 80 * i);
  });
}

// ── Checklist ──
function renderChecklist(step) {
  const saved = JSON.parse(localStorage.getItem('karman_checklist') || '{}');
  const allItems = step.categories.flatMap(c => c.items);
  const checkedCount = Object.values(saved).filter(Boolean).length;

  body.innerHTML = `
    <div class="checklist-progress-wrap">
      <div class="checklist-progress-header">
        <span>Documents ready</span>
        <strong id="checkCount">${checkedCount} of ${allItems.length}</strong>
      </div>
      <div class="checklist-progress-track">
        <div class="checklist-progress-fill" id="checkFill" style="width:${Math.round(checkedCount/allItems.length*100)}%"></div>
      </div>
    </div>
    ${step.categories.map(cat => `
      <div class="checklist-category">
        <div class="checklist-category__title">${cat.title}</div>
        <div class="checklist-items">
          ${cat.items.map(item => `
            <button class="checklist-item ${saved[item.id] ? 'checked' : ''}" data-id="${item.id}" type="button">
              <span class="checklist-item__box"></span>
              <span class="checklist-item__text">${item.text}</span>
            </button>
          `).join('')}
        </div>
      </div>
    `).join('')}
  `;

  nextBtn.textContent = 'Download checklist (PDF) →';
  updateProgress(50, 'Step 1 of 2');

  body.querySelectorAll('.checklist-item').forEach(btn => {
    btn.addEventListener('click', () => {
      btn.classList.toggle('checked');
      const id = btn.dataset.id;
      const current = JSON.parse(localStorage.getItem('karman_checklist') || '{}');
      current[id] = btn.classList.contains('checked');
      localStorage.setItem('karman_checklist', JSON.stringify(current));

      const total   = body.querySelectorAll('.checklist-item').length;
      const checked = body.querySelectorAll('.checklist-item.checked').length;
      document.getElementById('checkCount').textContent = `${checked} of ${total}`;
      document.getElementById('checkFill').style.width = `${Math.round(checked/total*100)}%`;
    });
  });
}

// ── Capture ──
function renderCapture(step) {
  body.innerHTML = `
    <div class="wizard-capture">
      <h3 class="wizard-capture__heading">${step.heading}</h3>
      <p class="wizard-capture__sub">${step.sub}</p>
      <div class="form-group">
        <label for="tool-name">Full name</label>
        <input type="text" id="tool-name" placeholder="Jane Smith" autocomplete="name" />
      </div>
      <div class="form-group">
        <label for="tool-email">Email address</label>
        <input type="email" id="tool-email" placeholder="jane@company.com" autocomplete="email" />
      </div>
      ${step.extraFields || ''}
    </div>`;

  nextBtn.textContent = step.ctaText || 'Submit →';

  body.querySelector('#tool-name').addEventListener('keydown', e => { if (e.key === 'Enter') advance(); });
  body.querySelector('#tool-email').addEventListener('keydown', e => { if (e.key === 'Enter') advance(); });
}

// ── Load jsPDF on demand ──
function loadJsPDF() {
  return new Promise((resolve, reject) => {
    if (window.jspdf && window.jspdf.jsPDF) { resolve(window.jspdf.jsPDF); return; }
    const s = document.createElement('script');
    s.src = 'https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js';
    s.onload = () => resolve(window.jspdf.jsPDF);
    s.onerror = () => reject(new Error('PDF library failed to load'));
    document.head.appendChild(s);
  });
}

// ── Generate PDF and return base64 + metadata ──
function buildPDF(jsPDF) {
  const doc = new jsPDF({ orientation: 'portrait', unit: 'mm', format: 'a4' });
  const W = 210, M = 18;
  let y = 0;

  // Header bar
  doc.setFillColor(10, 37, 64);
  doc.rect(0, 0, W, 28, 'F');
  doc.setFont('helvetica', 'bold');
  doc.setFontSize(18);
  doc.setTextColor(255, 255, 255);
  doc.text('KARMAN', M, 13);
  doc.setFont('helvetica', 'normal');
  doc.setFontSize(8);
  doc.setTextColor(160, 190, 215);
  doc.text('CORPORATE SERVICES SINGAPORE', M, 21);
  // Gold accent
  doc.setFillColor(201, 146, 42);
  doc.rect(0, 28, W, 1.5, 'F');
  y = 40;

  let subject = '', adminSummary = '';

  switch (state.toolId) {

    case 'businessStructure': {
      const result = TOOLS.businessStructure.getResult(state.answers);
      subject = 'Your Business Structure Recommendation — Karman';
      adminSummary = `Recommended: ${result.structure}\nOwnership: ${state.answers[0]}, Residency: ${state.answers[1]}, Liability: ${state.answers[2]}, Funding: ${state.answers[3]}, Growth: ${state.answers[4]}`;

      doc.setFont('helvetica', 'bold'); doc.setFontSize(16); doc.setTextColor(10, 37, 64);
      doc.text('Business Structure Recommendation', M, y); y += 7;
      doc.setFont('helvetica', 'normal'); doc.setFontSize(10); doc.setTextColor(107, 114, 128);
      doc.text(`Prepared for: ${state.answers.name}`, M, y); y += 12;

      // Result card
      doc.setFillColor(235, 243, 253);
      doc.roundedRect(M, y, W - M * 2, 36, 3, 3, 'F');
      doc.setFont('helvetica', 'bold'); doc.setFontSize(13); doc.setTextColor(10, 37, 64);
      doc.text(result.structure, M + 8, y + 10);
      doc.setFillColor(0, 178, 137);
      doc.roundedRect(M + 8, y + 13, 30, 6, 2, 2, 'F');
      doc.setFont('helvetica', 'bold'); doc.setFontSize(8); doc.setTextColor(255, 255, 255);
      doc.text(result.badge, M + 23, y + 17.5, { align: 'center' });
      doc.setFont('helvetica', 'normal'); doc.setFontSize(9); doc.setTextColor(55, 65, 81);
      const descLines = doc.splitTextToSize(result.desc, W - M * 2 - 16);
      doc.text(descLines, M + 8, y + 24);
      y += 42;

      doc.setFont('helvetica', 'bold'); doc.setFontSize(11); doc.setTextColor(10, 37, 64);
      doc.text('Key Advantages', M, y); y += 7;
      result.features.forEach(f => {
        doc.setFillColor(201, 146, 42);
        doc.circle(M + 2.5, y - 1.5, 1.3, 'F');
        doc.setFont('helvetica', 'normal'); doc.setFontSize(10); doc.setTextColor(55, 65, 81);
        doc.text(f, M + 7, y); y += 7;
      });
      break;
    }

    case 'costCalculator': {
      const services = state.answers[0] || [];
      const revenue = state.answers.revenue || 150000;
      const employees = state.answers.employees || 5;
      const pricing = {
        incorporation: { label: 'Company Incorporation', min: 699,  max: 2800 },
        secretary:     { label: 'Corporate Secretary',   min: 350,  max: 1500 },
        tax:           { label: 'Corporate Tax Filing',  min: 300,  max: 600  },
        gst:           { label: 'GST Registration & Filing', min: 400, max: 700 }
      };
      const breakdown = [];
      let tMin = 0, tMax = 0;
      services.forEach(s => {
        if (pricing[s]) { breakdown.push(pricing[s]); tMin += pricing[s].min; tMax += pricing[s].max; }
        if (s === 'accounting') {
          const [mn, mx] = revenue <= 150000 ? [900, 1200] : revenue <= 500000 ? [1800, 2400] : [3600, 4800];
          breakdown.push({ label: 'Accounting & Bookkeeping', min: mn, max: mx });
          tMin += mn; tMax += mx;
        }
        if (s === 'payroll') {
          const mn = employees * 300, mx = employees * 500;
          breakdown.push({ label: `Payroll (${employees} employee${employees > 1 ? 's' : ''})`, min: mn, max: mx });
          tMin += mn; tMax += mx;
        }
      });
      subject = 'Your Fee Estimate — Karman Corporate Services';
      adminSummary = `Services: ${services.join(', ')}\nRevenue: S$${revenue.toLocaleString()}\nEmployees: ${employees}\nEstimate: S$${tMin.toLocaleString()}–S$${tMax.toLocaleString()}`;

      doc.setFont('helvetica', 'bold'); doc.setFontSize(16); doc.setTextColor(10, 37, 64);
      doc.text('Annual Fee Estimate', M, y); y += 7;
      doc.setFont('helvetica', 'normal'); doc.setFontSize(10); doc.setTextColor(107, 114, 128);
      doc.text(`Prepared for: ${state.answers.name}`, M, y); y += 12;

      // Total box
      doc.setFillColor(10, 37, 64);
      doc.roundedRect(M, y, W - M * 2, 22, 3, 3, 'F');
      doc.setTextColor(160, 190, 215); doc.setFont('helvetica', 'normal'); doc.setFontSize(9);
      doc.text('ESTIMATED ANNUAL FEES (SGD)', M + 8, y + 7);
      doc.setTextColor(255, 255, 255); doc.setFont('helvetica', 'bold'); doc.setFontSize(17);
      doc.text(`S$${tMin.toLocaleString()} – S$${tMax.toLocaleString()}`, M + 8, y + 17);
      y += 30;

      // Table header
      doc.setFont('helvetica', 'bold'); doc.setFontSize(11); doc.setTextColor(10, 37, 64);
      doc.text('Fee Breakdown', M, y); y += 7;
      doc.setFillColor(235, 243, 253);
      doc.rect(M, y - 4, W - M * 2, 7, 'F');
      doc.setFont('helvetica', 'bold'); doc.setFontSize(9); doc.setTextColor(55, 65, 81);
      doc.text('Service', M + 3, y);
      doc.text('Range (S$)', W - M - 3, y, { align: 'right' });
      y += 6;

      breakdown.forEach((b, i) => {
        if (i % 2 === 0) { doc.setFillColor(249, 250, 251); doc.rect(M, y - 3.5, W - M * 2, 7, 'F'); }
        doc.setFont('helvetica', 'normal'); doc.setFontSize(9); doc.setTextColor(55, 65, 81);
        doc.text(b.label, M + 3, y);
        doc.text(`${b.min.toLocaleString()} – ${b.max.toLocaleString()}`, W - M - 3, y, { align: 'right' });
        y += 7;
      });

      // Total row
      doc.setFillColor(201, 146, 42);
      doc.rect(M, y - 3.5, W - M * 2, 8, 'F');
      doc.setFont('helvetica', 'bold'); doc.setFontSize(9); doc.setTextColor(255, 255, 255);
      doc.text('TOTAL (estimated)', M + 3, y + 1);
      doc.text(`${tMin.toLocaleString()} – ${tMax.toLocaleString()}`, W - M - 3, y + 1, { align: 'right' });
      y += 14;

      doc.setFont('helvetica', 'italic'); doc.setFontSize(8); doc.setTextColor(107, 114, 128);
      doc.text('All prices in SGD, excluding GST. Government filing fees included. Exact pricing confirmed after consultation.', M, y);
      break;
    }

    case 'eligibilityChecker': {
      const a = state.answers;
      const notes = [];
      if (a[2] === 'no')  notes.push('You\'ll need a nominee director — Karman can provide this service.');
      if (a[4] === 'yes') notes.push('Your activity may require additional licences (MAS, MOH, or another authority).');
      if (a[5] === 'no')  notes.push('We can check name availability on ACRA before submitting your application.');
      if (a[6] === 'no')  notes.push('Use our Document Checklist to track which documents you still need.');
      const eligible = notes.length === 0;
      subject = 'Your Singapore Eligibility Assessment — Karman';
      adminSummary = `Status: ${eligible ? 'Eligible' : 'Conditional'}\nNotes: ${notes.join(' | ') || 'None'}`;

      doc.setFont('helvetica', 'bold'); doc.setFontSize(16); doc.setTextColor(10, 37, 64);
      doc.text('Eligibility Assessment Report', M, y); y += 7;
      doc.setFont('helvetica', 'normal'); doc.setFontSize(10); doc.setTextColor(107, 114, 128);
      doc.text(`Prepared for: ${state.answers.name}`, M, y); y += 12;

      const [r, g, b2] = eligible ? [0, 178, 137] : [245, 158, 11];
      doc.setFillColor(r, g, b2);
      doc.roundedRect(M, y, W - M * 2, 18, 3, 3, 'F');
      doc.setFont('helvetica', 'bold'); doc.setFontSize(13); doc.setTextColor(255, 255, 255);
      doc.text(eligible ? '✓  You\'re eligible to incorporate!' : '⚠  Eligible — with a few things to sort', M + 8, y + 11.5);
      y += 26;

      doc.setFont('helvetica', 'normal'); doc.setFontSize(10); doc.setTextColor(55, 65, 81);
      const intro = eligible
        ? 'Based on your answers, you meet all basic requirements to register a Singapore Pte Ltd. Karman can get you incorporated in as little as 48 hours.'
        : 'You can still incorporate — there are just a few action items to sort first. Karman\'s team can guide you through each one.';
      const introLines = doc.splitTextToSize(intro, W - M * 2);
      doc.text(introLines, M, y); y += introLines.length * 6 + 8;

      if (notes.length) {
        doc.setFont('helvetica', 'bold'); doc.setFontSize(11); doc.setTextColor(10, 37, 64);
        doc.text('Action Items', M, y); y += 7;
        notes.forEach(n => {
          doc.setFillColor(245, 158, 11);
          doc.circle(M + 2.5, y - 1.5, 1.3, 'F');
          doc.setFont('helvetica', 'normal'); doc.setFontSize(10); doc.setTextColor(55, 65, 81);
          const lines = doc.splitTextToSize(n, W - M * 2 - 10);
          doc.text(lines, M + 7, y); y += lines.length * 6 + 3;
        });
      }
      break;
    }

    case 'timelineVisualizer': {
      subject = 'Your Singapore Incorporation Timeline — Karman';
      adminSummary = `Tool: Timeline Visualizer\nName: ${state.answers.name}`;

      doc.setFont('helvetica', 'bold'); doc.setFontSize(16); doc.setTextColor(10, 37, 64);
      doc.text('Incorporation Timeline', M, y); y += 7;
      doc.setFont('helvetica', 'normal'); doc.setFontSize(10); doc.setTextColor(107, 114, 128);
      doc.text('From idea to registered Singapore company — step by step', M, y); y += 14;

      TOOLS.timelineVisualizer.steps[0].items.forEach((item, i, arr) => {
        doc.setFillColor(10, 37, 64);
        doc.circle(M + 3, y - 1, 2.5, 'F');
        if (i < arr.length - 1) {
          doc.setDrawColor(200, 210, 220); doc.setLineWidth(0.5);
          doc.line(M + 3, y + 2, M + 3, y + 13);
        }
        doc.setFont('helvetica', 'bold'); doc.setFontSize(9); doc.setTextColor(201, 146, 42);
        doc.text(item.timing, M + 10, y);
        doc.setTextColor(10, 37, 64);
        doc.text(item.title, M + 32, y);
        y += 5.5;
        doc.setFont('helvetica', 'normal'); doc.setFontSize(8.5); doc.setTextColor(107, 114, 128);
        const lines = doc.splitTextToSize(item.desc, W - M * 2 - 12);
        doc.text(lines, M + 10, y); y += lines.length * 5 + 5;
      });
      break;
    }

    case 'documentChecklist': {
      subject = 'Your Incorporation Document Checklist — Karman';
      adminSummary = `Tool: Document Checklist\nName: ${state.answers.name}`;

      doc.setFont('helvetica', 'bold'); doc.setFontSize(16); doc.setTextColor(10, 37, 64);
      doc.text('Incorporation Document Checklist', M, y); y += 7;
      doc.setFont('helvetica', 'normal'); doc.setFontSize(10); doc.setTextColor(107, 114, 128);
      doc.text(`Prepared for: ${state.answers.name}`, M, y); y += 12;

      TOOLS.documentChecklist.steps[0].categories.forEach(cat => {
        if (y > 248) { doc.addPage(); y = 20; }
        doc.setFillColor(235, 243, 253);
        doc.rect(M, y - 4, W - M * 2, 8, 'F');
        doc.setFont('helvetica', 'bold'); doc.setFontSize(10); doc.setTextColor(10, 37, 64);
        doc.text(cat.title, M + 3, y); y += 9;

        cat.items.forEach(item => {
          if (y > 272) { doc.addPage(); y = 20; }
          doc.setDrawColor(150, 160, 170); doc.setLineWidth(0.4);
          doc.rect(M + 2, y - 3.5, 4, 4);
          doc.setFont('helvetica', 'normal'); doc.setFontSize(9); doc.setTextColor(55, 65, 81);
          const lines = doc.splitTextToSize(item.text, W - M * 2 - 12);
          doc.text(lines, M + 9, y); y += lines.length * 5.5 + 2;
        });
        y += 4;
      });
      break;
    }
  }

  // Footer on every page
  const pages = doc.internal.getNumberOfPages();
  for (let i = 1; i <= pages; i++) {
    doc.setPage(i);
    doc.setFillColor(10, 37, 64);
    doc.rect(0, 285, W, 12, 'F');
    doc.setFont('helvetica', 'normal'); doc.setFontSize(7.5); doc.setTextColor(160, 190, 215);
    doc.text('Karman Corporate Services Pte Ltd  ·  60 Paya Lebar Road, #06-28, Paya Lebar Square, Singapore 409051  ·  team@karman.com.sg  ·  +65 9138 2994', W / 2, 292, { align: 'center' });
  }

  const pdfBase64 = doc.output('datauristring').split(',')[1];
  return { pdfBase64, subject, adminSummary };
}

// ── Submit: generate PDF, send email, show result ──
async function simulateSubmit() {
  const btn = nextBtn;
  btn.textContent = 'Generating…';
  btn.disabled = true;

  try {
    const jsPDF = await loadJsPDF();
    const { pdfBase64, subject, adminSummary } = buildPDF(jsPDF);

    const res = await fetch('/api/send-result', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        toolId: state.toolId,
        userName: state.answers.name,
        userEmail: state.answers.email,
        subject,
        pdfBase64,
        adminSummary
      })
    });

    if (!res.ok) throw new Error('Send failed');

    btn.disabled = false;
    if (state.toolId === 'businessStructure') {
      renderFinalResult(TOOLS.businessStructure.getResult(state.answers));
    } else {
      renderGenericSuccess();
    }
    updateProgress(100, 'Complete');
    nextBtn.textContent = MODE === 'modal' ? 'Close →' : 'Done ✓';
    nextBtn.onclick = MODE === 'modal' ? closeTool : null;
    backBtn.classList.remove('visible');

  } catch (err) {
    btn.disabled = false;
    btn.textContent = nextBtn.dataset.originalText || 'Submit →';
    showToolError('Something went wrong. Please try again or email us at team@karman.com.sg');
  }
}

// ── Final Result: Business Structure ──
function renderFinalResult(result) {
  body.innerHTML = `
    <div class="wizard-result">
      <div class="wizard-result__icon">${result.icon}</div>
      <div class="wizard-result__badge wizard-result__badge--${result.badgeType}">${result.badge}</div>
      <div class="wizard-result__title">${result.structure}</div>
      <p class="wizard-result__desc">${result.desc}</p>
      <div class="wizard-result__features">
        ${result.features.map(f => `<div class="wizard-result__feature">${f}</div>`).join('')}
      </div>
      <p style="font-size:13px;color:var(--gray-400);text-align:center;">Full recommendation sent to <strong>${state.answers.email}</strong></p>
    </div>`;
}

// ── Generic success (quote / checklist / consultation) ──
function renderGenericSuccess() {
  const messages = {
    costCalculator:     { icon: '📄', title: 'Fee estimate sent!',        desc: `Your itemised fee estimate PDF has been sent to <strong>${state.answers.email}</strong>. An advisor will follow up within 1 business day.` },
    eligibilityChecker: { icon: '📄', title: 'Eligibility report sent!',  desc: `Your eligibility assessment PDF has been sent to <strong>${state.answers.email}</strong>. We'll be in touch to help with next steps.` },
    documentChecklist:  { icon: '📄', title: 'Checklist sent!',           desc: `Your document checklist PDF has been sent to <strong>${state.answers.email}</strong>. We'll be in touch shortly.` },
    timelineVisualizer: { icon: '📄', title: 'Timeline sent!',            desc: `Your incorporation timeline PDF has been sent to <strong>${state.answers.email}</strong>. Ready to start? Our team will reach out within 1 business day.` }
  };
  const msg = messages[state.toolId] || { icon: '📄', title: 'Sent!', desc: `Your report has been sent to <strong>${state.answers.email}</strong>.` };

  body.innerHTML = `
    <div class="wizard-result">
      <div class="wizard-result__icon">${msg.icon}</div>
      <div class="wizard-result__title">${msg.title}</div>
      <p class="wizard-result__desc">${msg.desc}</p>
    </div>`;
}

/* ══════════════════════════════════════════
   UTILITIES
══════════════════════════════════════════ */

function updateProgress(pct, text) {
  bar.style.width = pct + '%';
  label.textContent = text || '';
}

function showToolError(msg) {
  clearError();
  const div = document.createElement('div');
  div.className = 'tool-error';
  div.id = 'toolError';
  div.innerHTML = `⚠️ ${msg}`;
  body.appendChild(div);
}

function clearError() {
  const err = document.getElementById('toolError');
  if (err) err.remove();
}

function formatNum(n) {
  return Number(n).toLocaleString('en-SG');
}

function updateSliderFill(slider) {
  const min = +slider.min, max = +slider.max, val = +slider.value;
  const pct = ((val - min) / (max - min)) * 100;
  slider.style.background = `linear-gradient(to right, var(--blue) 0%, var(--blue) ${pct}%, var(--gray-200) ${pct}%, var(--gray-200) 100%)`;
}

// ── Scroll lock (iOS-safe) ──
let _scrollY = 0;
function lockScroll() {
  _scrollY = window.scrollY;
  document.body.style.position = 'fixed';
  document.body.style.top = `-${_scrollY}px`;
  document.body.style.width = '100%';
}
function unlockScroll() {
  document.body.style.position = '';
  document.body.style.top = '';
  document.body.style.width = '';
  window.scrollTo(0, _scrollY);
}

// ── Focus trap (modal mode only) ──
function trapFocus() {
  if (MODE !== 'modal' || !modal) return;
  const panel = modal.querySelector('.tool-modal__panel');
  const focusable = [...panel.querySelectorAll('button:not([disabled]), input, select, textarea, a[href], [tabindex]:not([tabindex="-1"])')];
  if (!focusable.length) return;
  focusable[0].focus();
  panel._trapHandler && panel.removeEventListener('keydown', panel._trapHandler);
  panel._trapHandler = (e) => {
    if (e.key !== 'Tab') return;
    const first = focusable[0], last = focusable[focusable.length - 1];
    if (e.shiftKey) { if (document.activeElement === first) { e.preventDefault(); last.focus(); } }
    else { if (document.activeElement === last) { e.preventDefault(); first.focus(); } }
  };
  panel.addEventListener('keydown', panel._trapHandler);
}

/* ══════════════════════════════════════════
   EVENT LISTENERS
══════════════════════════════════════════ */

if (MODE === 'modal') {
  // Launch buttons → open modal
  document.querySelectorAll('.tool-launch-btn').forEach(btn => {
    btn.addEventListener('click', () => openTool(btn.dataset.tool, btn));
  });
  modal.querySelector('.tool-modal__close').addEventListener('click', closeTool);
  modal.querySelector('.tool-modal__backdrop').addEventListener('click', closeTool);
  nextBtn.addEventListener('click', advance);
  backBtn.addEventListener('click', goBack);
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && modal.classList.contains('tool-modal--open')) closeTool();
  });
}

if (MODE === 'inline') {
  // Auto-initialize inline tool
  const toolId = INLINE_ROOT.dataset.tool;
  if (TOOLS[toolId]) {
    state = { toolId, step: 0, history: [], answers: {}, triggerEl: null };
    const tool = TOOLS[toolId];
    if (title) title.textContent = tool.title;
    if (tag)   tag.textContent   = tool.tag;
    nextBtn.addEventListener('click', advance);
    backBtn.addEventListener('click', goBack);
    renderStep();
  }
}
