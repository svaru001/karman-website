const fs = require('fs');
const path = require('path');

const blogDir = path.join(__dirname, '../blog');

// HowTo schema definitions for process posts
const HOWTO = {
  'how-to-incorporate-company-singapore-foreigner': {
    name: 'How to Incorporate a Company in Singapore as a Foreigner',
    description: 'Step-by-step guide for foreign founders to register a Singapore Pte Ltd company.',
    steps: [
      { name: 'Choose a company name', text: 'Search ACRA\'s BizFile+ to confirm the name is available and not similar to existing companies. Avoid restricted words that require additional approval (e.g. "bank", "finance", "school").' },
      { name: 'Appoint a local resident director', text: 'Singapore requires at least one director who is ordinarily resident in Singapore — either a Singapore citizen, PR, or holder of an EntrePass or Employment Pass. If you do not have a local director, appoint a nominee director.' },
      { name: 'Prepare incorporation documents', text: 'Prepare the company constitution, director and shareholder particulars, passport copies, and proof of residential address. Foreign shareholders require certified true copies or notarisation depending on the country.' },
      { name: 'File with ACRA via a registered filing agent', text: 'Submit incorporation documents through an ACRA-registered Corporate Service Provider (CSP). ACRA typically approves within 1–3 business days. The government fee is S$315 (name application S$15 + incorporation S$300).' },
      { name: 'Open a corporate bank account', text: 'After receiving your ACRA Certificate of Incorporation, apply for a Singapore corporate bank account. Most banks require in-person or video verification. Processing takes 4–8 weeks depending on the bank.' },
    ]
  },
  'how-to-incorporate-vcc-singapore': {
    name: 'How to Incorporate a Variable Capital Company (VCC) in Singapore',
    description: 'Step-by-step guide to setting up a Singapore VCC for fund management.',
    steps: [
      { name: 'Appoint a MAS-licensed fund manager', text: 'A Singapore VCC must be managed by a fund manager holding a Capital Markets Services (CMS) licence from MAS, or be an exempt fund manager (RFMC or A-CIS). You must appoint this fund manager before or at the time of VCC incorporation.' },
      { name: 'Choose VCC structure: standalone or umbrella', text: 'A standalone VCC is a single fund entity. An umbrella VCC can have multiple sub-funds with segregated assets and liabilities under one corporate shell — ideal for multi-strategy or multi-investor mandates.' },
      { name: 'File VCC incorporation with ACRA', text: 'File via an ACRA-registered CSP using the VCC-specific incorporation form. The VCC constitution must comply with the Variable Capital Companies Act. Incorporation typically takes 1–3 business days. The government fee is S$315.' },
      { name: 'Apply for 13O or 13U tax incentive (optional)', text: 'Apply to MAS for tax exemption on qualifying investment income. 13O requires a minimum S$10 million AUM. 13U requires S$50 million AUM and at least one investment professional. MAS review takes 4–8 weeks.' },
      { name: 'Open VCC bank account and onboard investors', text: 'Open a corporate bank account in the VCC\'s name. Draft the fund\'s subscription documents, side letters, and AML/KYC procedures before accepting capital from investors.' },
    ]
  },
  'how-to-close-company-singapore': {
    name: 'How to Close a Company in Singapore',
    description: 'Step-by-step process to strike off or wind up a Singapore Pte Ltd company.',
    steps: [
      { name: 'Settle all liabilities and cease operations', text: 'Ensure all outstanding debts, taxes, CPF contributions, and employee obligations are fully settled. File all overdue ACRA annual returns and IRAS tax returns before applying for strike-off.' },
      { name: 'Pass a members\' resolution to close', text: 'Pass a directors\' or members\' resolution agreeing to close the company. For solvent companies with fewer than 3 creditors, the simplified strike-off route via ACRA is typically the fastest option.' },
      { name: 'Apply for ACRA strike-off (for solvent companies)', text: 'Submit the strike-off application through BizFile+. ACRA charges S$33. ACRA will notify known creditors. If no objections are received within 60 days, ACRA strikes the company off the register and the company ceases to exist.' },
      { name: 'Voluntary winding up (for companies with creditors)', text: 'If the company has significant creditors, appoint a licensed insolvency practitioner to conduct a creditors\' voluntary winding up. This involves a formal liquidation process, realisation of assets, and distribution to creditors before dissolution.' },
      { name: 'Close bank accounts and surrender licences', text: 'After dissolution is confirmed, close all corporate bank accounts and surrender any business licences, GST registration, or employment passes sponsored by the company.' },
    ]
  },
  'how-long-does-singapore-company-incorporation-take': {
    name: 'How to Incorporate a Singapore Company (Timeline)',
    description: 'Overview of the incorporation timeline and each stage of setting up a Singapore Pte Ltd.',
    steps: [
      { name: 'Name reservation (same day)', text: 'Submit a name application through ACRA BizFile+. Routine names are approved instantly or within 1 business day. Names requiring ministerial approval (e.g. containing "bank" or "school") take 14–60 days.' },
      { name: 'Document preparation (1–3 days)', text: 'Gather passport copies, proof of address, and draft the company constitution. Foreign founders may need certified true copies. Your CSP prepares the ACRA filing package.' },
      { name: 'ACRA incorporation filing (1–3 business days)', text: 'Submit the incorporation application through an ACRA-registered CSP. Most straightforward Pte Ltd applications are approved within 1–3 business days. You receive the Certificate of Incorporation by email.' },
      { name: 'Post-incorporation setup (1–2 weeks)', text: 'After incorporation, open a corporate bank account, register for GST (if revenue exceeds S$1 million), set up CPF contributions, and appoint an auditor if required. Your CSP also prepares the statutory registers and share certificates.' },
      { name: 'Bank account opening (4–8 weeks)', text: 'Corporate bank account opening is the longest step. Most Singapore banks require an in-person or video meeting with directors and take 4–8 weeks to complete due diligence. Total time from starting to fully operational: 6–10 weeks.' },
    ]
  },
  'singapore-bank-account-foreign-company': {
    name: 'How to Open a Singapore Corporate Bank Account as a Foreign Company',
    description: 'Step-by-step guide for foreign founders and companies to open a Singapore business bank account.',
    steps: [
      { name: 'Incorporate your Singapore company first', text: 'Most banks require an ACRA Certificate of Incorporation before accepting a bank account application. Ensure your company has been registered with ACRA and has a valid UEN number.' },
      { name: 'Choose the right bank', text: 'Major options include DBS, OCBC, UOB (local banks), and Standard Chartered, HSBC, Citibank (international banks). Local banks offer faster SME account opening. International banks suit companies with complex cross-border structures but require higher minimum deposits.' },
      { name: 'Prepare KYC documentation', text: 'Prepare: ACRA BizFile+ company profile, Certificate of Incorporation, company constitution, passport copies of all directors and UBOs, proof of residential address, business plan or website, and source of funds declaration. Foreign directors may need notarised or apostilled documents.' },
      { name: 'Submit application and attend verification', text: 'Submit the application online or in person. Most banks require at least one director to attend an in-person or video call verification. Some digital banks (Airwallex, Aspire, Wise) allow fully remote onboarding for eligible businesses.' },
      { name: 'Await approval (4–8 weeks)', text: 'Banks conduct AML/KYC due diligence which takes 4–8 weeks for traditional banks, or 1–2 weeks for digital banking alternatives. Approval is not guaranteed — banks assess business activity, ownership structure, and source of funds.' },
    ]
  },
  'when-to-register-gst-singapore': {
    name: 'How to Register for GST in Singapore',
    description: 'Step-by-step guide to GST registration for Singapore businesses.',
    steps: [
      { name: 'Check if you are required to register', text: 'GST registration is mandatory when your taxable turnover exceeds S$1 million in the past 12 months, or is expected to exceed S$1 million in the next 12 months. Voluntary registration is available for businesses below this threshold that want to claim GST input tax.' },
      { name: 'Prepare supporting documents', text: 'Gather your company\'s ACRA profile, financial statements or revenue projections, bank statements, and a description of your business activities. IRAS may request additional supporting documents based on your industry.' },
      { name: 'Submit GST registration application to IRAS', text: 'Apply online via myTax Portal using Corppass. For mandatory registration, apply within 30 days of the date you became liable to register. Backdated registration and penalties apply if you miss this deadline.' },
      { name: 'Receive GST registration number', text: 'IRAS typically processes GST applications within 10 business days. You will receive a GST registration number and an effective registration date. From this date, you must charge 9% GST on all taxable supplies.' },
      { name: 'File quarterly GST returns', text: 'File GST F5 returns quarterly (or monthly for large businesses) via myTax Portal. Returns are due within 1 month of the end of each accounting period. Late filing and late payment attract penalties and interest.' },
    ]
  },
  'singapore-company-annual-compliance-checklist': {
    name: 'How to Complete Annual Compliance for a Singapore Company',
    description: 'Annual compliance checklist for Singapore Pte Ltd companies.',
    steps: [
      { name: 'Hold Annual General Meeting (AGM)', text: 'Private companies with a financial year ending on or after 31 August 2018 are exempt from holding AGMs if they send financial statements to shareholders within 5 months of financial year end. Companies that are not exempt must hold their AGM within 6 months of financial year end.' },
      { name: 'File annual return with ACRA', text: 'File the Annual Return via BizFile+ within 7 months of your financial year end. The filing fee is S$60. The Annual Return confirms your company\'s registered details, directors, shareholders, and share capital are up to date.' },
      { name: 'File corporate income tax return with IRAS', text: 'File Form C-S or Form C with IRAS by 30 November each year. Form C-S applies to companies with revenue below S$5 million with straightforward tax affairs. Estimated Chargeable Income (ECI) must be filed within 3 months of your financial year end.' },
      { name: 'Renew business licences if applicable', text: 'Check whether your business holds any licences or permits that require annual renewal — e.g. food establishment licence, financial adviser licence, employment agency licence. Renewal timelines vary by licence type.' },
      { name: 'Update company records and registers', text: 'Ensure statutory registers are up to date: Register of Directors, Register of Members, Register of Nominee Directors (ROND), and Register of Nominee Shareholders (RONS) if applicable. Any changes must be filed with ACRA within 14 days.' },
    ]
  },
};

function injectHowTo(html, slug) {
  const def = HOWTO[slug];
  if (!def) return null;
  if (html.includes('"HowTo"')) return null; // already has it

  const steps = def.steps.map((s, i) => `      {
        "@type": "HowToStep",
        "position": ${i + 1},
        "name": ${JSON.stringify(s.name)},
        "text": ${JSON.stringify(s.text)}
      }`).join(',\n');

  const schema = `  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "HowTo",
    "name": ${JSON.stringify(def.name)},
    "description": ${JSON.stringify(def.description)},
    "step": [
${steps}
    ]
  }
  </script>`;

  return html.replace('</head>', schema + '\n</head>');
}

let processed = 0;
for (const slug of Object.keys(HOWTO)) {
  const filePath = path.join(blogDir, slug, 'index.html');
  if (!fs.existsSync(filePath)) { console.log(`⚠ Not found: ${slug}`); continue; }
  let html = fs.readFileSync(filePath, 'utf8');
  const updated = injectHowTo(html, slug);
  if (!updated) { console.log(`⚠ Skipped (already has HowTo): ${slug}`); continue; }
  fs.writeFileSync(filePath, updated);
  console.log(`✓ ${slug}`);
  processed++;
}
console.log(`\nDone: ${processed} HowTo schemas injected`);
