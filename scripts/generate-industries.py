#!/usr/bin/env python3
"""Generate Karman industry landing pages under /for/<slug>/index.html and the hub /for/index.html."""

import json
import html as htmlmod
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "for"

NAV_HTML = """  <header class="header" id="header">
    <nav class="nav container" aria-label="Main navigation">
      <a href="/" class="nav__logo"><img src="/logo.svg" alt="Karman" class="nav__logo-img" width="124" height="40" fetchpriority="high"></a>
      <ul class="nav__menu" id="navMenu">
        <li class="nav__item"><a href="/#services" class="nav__link">Services</a></li>
        <li class="nav__item"><a href="/about" class="nav__link">About</a></li>
        <li class="nav__item"><a href="/tools/" class="nav__link">Free Tools <span class="nav__badge">Free</span></a></li>
        <li class="nav__item"><a href="/blog" class="nav__link">Blog</a></li>
        <li class="nav__item"><a href="/#faq" class="nav__link">FAQ</a></li>
      <div class="nav__actions">
        <a href="/#contact" class="btn btn--secondary">Contact us</a>
        <a href="/#get-started" class="btn btn--primary">Get started</a>
      </div>
      <button class="nav__hamburger" id="hamburger" aria-label="Toggle menu"><span></span><span></span><span></span></button>
    </nav>
  </header>
"""

FOOTER_HTML = """  <footer class="footer">
    <div class="container">
      <div class="footer__top">
        <div class="footer__brand">
          <a href="/" class="nav__logo"><img src="/logo.svg" alt="Karman" class="nav__logo-img" width="124" height="40" loading="lazy"></a>
          <p>Trusted corporate services for Singapore businesses. ACRA Registered Filing Agent.</p>
          <div class="footer__badges"><span class="badge">ACRA Registered</span>  <a class="footer__social-link" href="https://www.linkedin.com/company/karman-advisory-singapore/" target="_blank" rel="noopener" aria-label="Karman on LinkedIn"><svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor" xmlns="http://www.w3.org/2000/svg"><path d="M20.45 20.45h-3.55v-5.57c0-1.33-.03-3.04-1.85-3.04-1.85 0-2.14 1.45-2.14 2.94v5.67H9.36V9h3.41v1.56h.05c.48-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.45v6.29zM5.34 7.43a2.06 2.06 0 1 1 0-4.12 2.06 2.06 0 0 1 0 4.12zM7.12 20.45H3.56V9h3.56v11.45zM22.22 0H1.77C.79 0 0 .77 0 1.72v20.56C0 23.23.79 24 1.77 24h20.45c.98 0 1.78-.77 1.78-1.72V1.72C24 .77 23.2 0 22.22 0z"/></svg></a>
          </div>
        </div>
        <div class="footer__links">
          <div class="footer-col"><h4>Services</h4><ul><li><a href="/#incorporation">Company Incorporation</a></li><li><a href="/#secretary">Corporate Secretarial</a></li><li><a href="/#accounting">Accounting</a></li></ul></div>
          <div class="footer-col"><h4>Free Resources</h4><ul><li><a href="/tools/">Free Tools</a></li><li><a href="/templates/">Templates</a></li><li><a href="/glossary/">Glossary</a></li><li><a href="/blog">Blog</a></li></ul></div>
          <div class="footer-col"><h4>Company</h4><ul><li><a href="/#about">About</a></li><li><a href="/#contact">Contact</a></li></ul></div>
        </div>
      </div>
      <div class="footer__bottom"><p>© 2026 Karman Corporate Services Pte Ltd. UEN: 202012889R. 60 Paya Lebar Road, #06-28, Paya Lebar Square, Singapore 409051.</p></div>
    </div>
  </footer>
"""

CSS = """    .ind-hero { background:linear-gradient(180deg,#fff 0%,#f7f9fc 100%); padding:60px 0 50px; border-bottom:1px solid var(--gray-200); }
    .ind-hero__breadcrumb { font-size:13px; color:var(--gray-600); margin-bottom:14px; }
    .ind-hero__breadcrumb a { color:var(--gray-700); text-decoration:none; }
    .ind-hero__breadcrumb a:hover { color:#0d4567; text-decoration:underline; }
    .ind-hero__breadcrumb span { margin:0 6px; color:var(--gray-400); }
    .ind-hero__pill { display:inline-block; font-size:11px; font-weight:700; text-transform:uppercase; letter-spacing:.5px; color:#0d4567; background:#e8f1f8; padding:5px 11px; border-radius:6px; margin-bottom:14px; }
    .ind-hero h1 { font-family:'Sora',sans-serif; font-size:clamp(30px,4.5vw,44px); line-height:1.15; color:#0A2540; margin:0 0 14px; max-width:820px; }
    .ind-hero__lede { font-size:18px; line-height:1.6; color:var(--gray-700); max-width:760px; margin:0 0 20px; }
    .ind-hero__cta { display:inline-flex; gap:12px; flex-wrap:wrap; margin-top:8px; }
    .ind-answer { background:#f0f7ff; border-left:4px solid #0d4567; border-radius:0 10px 10px 0; padding:18px 22px; margin:0 0 4px; max-width:820px; }
    .ind-answer p { margin:0; font-size:16px; line-height:1.65; color:#0A2540; }
    .ind-answer strong { color:#0d4567; }
    .ind-section { padding:50px 0; }
    .ind-section--gray { background:#f7f9fc; }
    .ind-section h2 { font-family:'Sora',sans-serif; font-size:clamp(24px,3vw,30px); color:#0A2540; margin:0 0 12px; }
    .ind-section__sub { color:var(--gray-700); font-size:16px; line-height:1.6; max-width:760px; margin:0 0 28px; }
    .ind-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(260px,1fr)); gap:18px; }
    .ind-card { background:#fff; border:1px solid var(--gray-200); border-radius:14px; padding:24px; }
    .ind-card h3 { font-family:'Sora',sans-serif; font-size:17px; color:#0A2540; margin:0 0 8px; display:flex; align-items:center; gap:10px; }
    .ind-card__icon { width:36px; height:36px; border-radius:9px; background:#e8f1f8; color:#0d4567; display:flex; align-items:center; justify-content:center; flex-shrink:0; }
    .ind-card p { font-size:14.5px; line-height:1.6; color:var(--gray-700); margin:0; }
    .ind-stack { display:flex; flex-direction:column; gap:14px; max-width:820px; }
    .ind-stack__item { background:#fff; border:1px solid var(--gray-200); border-radius:12px; padding:18px 22px; }
    .ind-stack__item h3 { font-family:'Sora',sans-serif; font-size:16.5px; color:#0A2540; margin:0 0 6px; }
    .ind-stack__item p { font-size:14.5px; line-height:1.6; color:var(--gray-700); margin:0; }
    .ind-recipe { background:#fff; border:1px solid var(--gray-200); border-radius:14px; padding:28px 32px; max-width:820px; }
    .ind-recipe h3 { font-family:'Sora',sans-serif; font-size:18px; color:#0d4567; margin:0 0 14px; }
    .ind-recipe ul { list-style:none; padding:0; margin:0; }
    .ind-recipe li { display:grid; grid-template-columns:140px 1fr; gap:16px; padding:10px 0; border-bottom:1px dashed var(--gray-200); font-size:15px; line-height:1.55; }
    .ind-recipe li:last-child { border-bottom:none; }
    .ind-recipe li strong { color:#0A2540; font-weight:600; }
    .ind-recipe li span { color:var(--gray-700); }
    .ind-ssic { display:flex; flex-wrap:wrap; gap:10px; max-width:820px; }
    .ind-ssic a { display:inline-flex; align-items:center; gap:8px; padding:10px 14px; background:#fff; border:1px solid var(--gray-200); border-radius:10px; text-decoration:none; color:#0A2540; font-size:14px; transition:all .15s; }
    .ind-ssic a:hover { border-color:#0d4567; transform:translateY(-1px); }
    .ind-ssic a code { font-family:'SF Mono','Monaco',monospace; font-size:12.5px; font-weight:700; color:#0d4567; background:#e8f1f8; padding:2px 7px; border-radius:5px; }
    .ind-faq { max-width:820px; }
    .ind-faq details { background:#fff; border:1px solid var(--gray-200); border-radius:10px; padding:16px 20px; margin-bottom:10px; }
    .ind-faq details[open] { border-color:#0d4567; }
    .ind-faq summary { font-weight:600; font-size:16px; color:#0A2540; cursor:pointer; list-style:none; }
    .ind-faq summary::-webkit-details-marker { display:none; }
    .ind-faq summary::before { content:"+ "; font-weight:700; color:#0d4567; }
    .ind-faq details[open] summary::before { content:"− "; }
    .ind-faq details > p { margin:12px 0 0; font-size:15px; line-height:1.65; color:var(--gray-700); }
    .ind-related { display:grid; grid-template-columns:repeat(auto-fill,minmax(240px,1fr)); gap:14px; }
    .ind-related a { display:block; background:#fff; border:1px solid var(--gray-200); border-radius:12px; padding:16px 18px; text-decoration:none; color:#0A2540; transition:all .15s; }
    .ind-related a:hover { border-color:#0d4567; transform:translateY(-1px); box-shadow:0 4px 12px rgba(13,69,103,.08); }
    .ind-related__label { display:inline-block; font-size:11px; font-weight:700; text-transform:uppercase; letter-spacing:.4px; color:#0d4567; margin-bottom:4px; }
    .ind-related__title { font-weight:700; font-size:15px; margin:0 0 4px; }
    .ind-related__desc { font-size:13.5px; line-height:1.5; color:var(--gray-700); margin:0; }
    .ind-cta { background:linear-gradient(135deg,#0A2540 0%,#0d4567 100%); border-radius:18px; padding:42px 44px; color:#fff; max-width:920px; margin:0 auto; }
    .ind-cta h2 { font-family:'Sora',sans-serif; font-size:26px; margin:0 0 10px; color:#fff; }
    .ind-cta p { font-size:16px; line-height:1.6; opacity:.92; margin:0 0 22px; max-width:640px; }
    .ind-cta .btn { background:#fff; color:#0d4567; padding:13px 26px; border-radius:8px; font-weight:700; text-decoration:none; display:inline-block; font-size:15px; transition:transform .15s; }
    .ind-cta .btn:hover { transform:translateY(-1px); }
    .ind-hub { padding:60px 0 80px; }
    .ind-hub h1 { font-family:'Sora',sans-serif; font-size:clamp(30px,4vw,42px); color:#0A2540; margin:0 0 12px; }
    .ind-hub__lede { font-size:18px; line-height:1.6; color:var(--gray-700); max-width:760px; margin:0 0 32px; }
    .ind-hub__grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(300px,1fr)); gap:18px; }
    .ind-hub__card { background:#fff; border:1px solid var(--gray-200); border-radius:14px; padding:24px 26px; text-decoration:none; color:inherit; display:flex; flex-direction:column; gap:10px; transition:all .15s; }
    .ind-hub__card:hover { border-color:#0d4567; transform:translateY(-2px); box-shadow:0 6px 18px rgba(13,69,103,.10); }
    .ind-hub__card-icon { width:42px; height:42px; border-radius:10px; background:#e8f1f8; color:#0d4567; display:flex; align-items:center; justify-content:center; }
    .ind-hub__card h3 { font-family:'Sora',sans-serif; font-size:18px; color:#0A2540; margin:0; }
    .ind-hub__card p { font-size:14.5px; line-height:1.55; color:var(--gray-700); margin:0; flex:1; }
    .ind-hub__card-cta { font-size:13.5px; font-weight:700; color:#0d4567; margin-top:auto; }
"""

INDUSTRIES = [
    {
        "slug": "ai-startups",
        "name": "AI Startups",
        "icon": "AI",
        "title": "Singapore Incorporation for AI Startups | Karman",
        "description": "Set up a Singapore Pte Ltd for your AI startup. IP protection, US/UK investor-friendly structure, R&D tax credits, EP for technical founders. From S$699.",
        "hero_h1": "Singapore incorporation for AI startups and founders",
        "hero_lede": "Hold IP, raise from US and Indian investors, and access Asia from a jurisdiction that VCs already understand. We handle the ACRA filing, post-incorporation paperwork, and ongoing compliance so you can ship.",
        "answer": "<strong>Most AI startups in Singapore incorporate as a private limited company (Pte Ltd)</strong> with a single share class and a holding-company-friendly cap table. Singapore offers strong IP enforcement, a 17% headline corporate tax with R&D super-deductions, and predictable Employment Pass routes for technical founders. Setup takes 1–3 business days through ACRA.",
        "why_singapore": [
            ("VC-recognized jurisdiction", "Sequoia, Lightspeed, Vertex, Insignia, B Capital, and most Asia-focused funds prefer Singapore Pte Ltd cap tables over offshore wrappers."),
            ("IP protection that holds up", "Singapore consistently ranks #1 in Asia for IP protection (WIPO). Software, model weights, and trade secrets are enforceable in Singapore courts."),
            ("R&D tax incentives", "Up to 250% tax deduction on qualifying R&D under Section 14C/14D - applies to ML research, software development, and prototype work."),
            ("Talent visas that work", "Tech.Pass, ONE Pass, and Employment Pass (EP) routes for technical founders and senior ML engineers. Tech.Pass is renewable for 2 years without an employer sponsor."),
        ],
        "structure_recipe": [
            ("Entity", "Singapore Pte Ltd (private limited)"),
            ("Share capital", "S$1 paid-up minimum; founders typically issue 10,000–1,000,000 ordinary shares"),
            ("Cap table", "Single class ordinary; SAFE/convertible-friendly; ESOP pool reserved (typically 10–15%)"),
            ("Directors", "≥1 ordinary resident director (Singapore citizen, PR, or EP holder)"),
            ("Holding company", "Optional Cayman or BVI parent if raising from a US fund that requires it; otherwise direct"),
            ("Bank", "Aspire, Wise Business, or DBS - Aspire fastest for foreign founders"),
        ],
        "ssic_codes": [
            ("62019", "Development of other software and programming activities"),
            ("63111", "Data processing, hosting and related activities"),
            ("72100", "Research and experimental development on natural sciences and engineering"),
            ("70201", "Business and management consultancy services"),
        ],
        "challenges": [
            ("Ordinary resident director requirement", "Foreign founders need at least one Singapore-resident director. Karman provides nominee director services from S$2,400/year while you secure your own EP."),
            ("Bank account opening for foreign founders", "Traditional banks require in-person verification. Aspire and Wise Business can open accounts remotely in 3–5 days; DBS typically requires a Singapore visit."),
            ("Choosing between direct Pte Ltd vs Cayman holdco", "If you're raising from a US-only fund (Sequoia US, a16z), they may require a Cayman parent with a Singapore subsidiary. Most Asia-focused funds prefer a clean Singapore Pte Ltd."),
            ("R&D claims documentation", "To claim 250% R&D super-deduction you need contemporaneous project documentation, time-tracking on R&D activities, and invoice evidence. Set this up from day one."),
        ],
        "faqs": [
            ("Should an AI startup incorporate in Singapore or Delaware?",
             "If your customers and investors are primarily US-based, Delaware C-Corp remains the default. If you're raising from Asia-focused VCs (Sequoia SEA, Vertex, Insignia, Lightspeed India), serving Asia customers, or want lower ongoing tax friction, Singapore Pte Ltd is the better choice. Some founders use a Cayman parent with a Singapore operating subsidiary to satisfy US fund requirements while operating from Singapore."),
            ("Does Singapore tax software revenue earned from foreign customers?",
             "Yes - Singapore taxes worldwide income at 17%, but Foreign-Sourced Income Exemption (FSIE) and the territorial-income rules can exempt income that is genuinely earned and kept abroad. Most SaaS and AI startups invoicing global customers from Singapore pay 17% on profits, but qualify for the Startup Tax Exemption (75% exemption on first S$100K of income for first 3 years)."),
            ("Can I get an Employment Pass as an AI startup founder?",
             "Yes. Employment Pass requires a minimum monthly salary of S$5,600 (S$10,500 in financial services) and points-based COMPASS assessment. Tech.Pass is an alternative for senior tech professionals - requires US$20K+ monthly salary OR 5+ years at a leading tech company OR a product with 100K+ users. ONE Pass requires S$30K monthly salary."),
            ("How do I protect AI model IP in Singapore?",
             "Software code is automatically protected by copyright. Trade secrets (model weights, training data, fine-tuning processes) are protected under common law and contract. Patents are available for novel ML architectures but rarely worth filing for typical applied-AI work. Karman's Mutual NDA template is the starting point for protecting trade secrets with contractors and vendors."),
            ("How long does it take to incorporate from outside Singapore?",
             "ACRA approval is typically 1–3 business days once we have your KYC documents. End-to-end (KYC + name reservation + filing + bank account) is 7–14 days for foreign founders. Karman handles the entire process remotely - no Singapore visit required for incorporation itself."),
        ],
        "related": [
            ("tool", "/tools/business-structure-recommender", "Structure Recommender", "Find the right entity for your AI startup."),
            ("tool", "/tools/cost-calculator", "Cost Calculator", "Estimate annual incorporation, secretary, and accounting fees."),
            ("tool", "/tools/eligibility-checker", "Eligibility Checker", "Check if you qualify to incorporate as a foreign founder."),
            ("template", "/templates/founders-agreement", "Founders' Agreement", "Lock in equity splits, vesting, and IP assignment."),
            ("template", "/templates/mutual-nda", "Mutual NDA", "Protect AI models, training data, and trade secrets."),
            ("term", "/glossary/pte-ltd", "Glossary: Pte Ltd", "What a private limited company is and isn't."),
            ("term", "/glossary/ep", "Glossary: Employment Pass", "Eligibility, salary thresholds, and COMPASS scoring."),
            ("term", "/glossary/section-13o", "Glossary: Section 13O", "Singapore's family office tax incentive (relevant if your investor uses one)."),
        ],
    },
    {
        "slug": "ecommerce",
        "name": "E-commerce",
        "icon": "EC",
        "title": "Singapore Incorporation for E-commerce Brands | Karman",
        "description": "Incorporate your e-commerce brand in Singapore. Cross-border tax efficiency, Stripe + payment gateway access, GST handling, regional warehouse strategy. From S$699.",
        "hero_h1": "Singapore incorporation for e-commerce and DTC brands",
        "hero_lede": "Sell across Southeast Asia, the US, and India from a single Pte Ltd with predictable tax, multi-currency banking, and GST handled correctly. Karman handles incorporation, monthly bookkeeping, and GST filing.",
        "answer": "<strong>Most e-commerce founders incorporate a Singapore Pte Ltd</strong> to access regional payment processors (Stripe, Adyen, NETS), open multi-currency bank accounts (Wise Business, Aspire, DBS), and benefit from Singapore's 0% GST on exports. Once turnover crosses S$1M, GST registration becomes mandatory. Setup takes 1–3 business days through ACRA.",
        "why_singapore": [
            ("Stripe and payment gateway access", "Stripe Singapore supports SGD, USD, and 135+ currencies. Adyen, NETS, GrabPay, ShopeePay all integrate cleanly. US-based gateways often hold funds for new merchants - Singapore equivalents settle T+2."),
            ("0% GST on exports", "Goods shipped outside Singapore are zero-rated. You charge no GST on US, EU, India, or non-Singapore APAC orders, and you can still claim back input GST on your Singapore costs."),
            ("Multi-currency banking", "Wise Business and Aspire give you SGD, USD, EUR, GBP, AUD account details from day one. DBS Multi-Currency Account adds JPY, CNY, INR, IDR, MYR, THB, VND."),
            ("Regional fulfillment hub", "Singapore is a 4-hour flight to Jakarta, Bangkok, Manila, Kuala Lumpur, and Ho Chi Minh. ASEAN Free Trade Area (AFTA) means 0% tariffs into most ASEAN destinations from Singapore."),
        ],
        "structure_recipe": [
            ("Entity", "Singapore Pte Ltd"),
            ("Share capital", "S$1 paid-up minimum; founders + early angels typically own 80–95%"),
            ("GST registration", "Voluntary at any turnover; mandatory once turnover exceeds S$1M (rolling 12-month basis)"),
            ("Directors", "≥1 ordinary resident director"),
            ("Bank", "Wise Business or Aspire for multi-currency; DBS once volume justifies relationship banking"),
            ("Payment gateway", "Stripe Singapore (default), Adyen for enterprise volume, GrabPay/ShopeePay for SEA marketplaces"),
        ],
        "ssic_codes": [
            ("47919", "Retail sale via Internet (excluding motor vehicles)"),
            ("46900", "Non-specialised wholesale trade"),
            ("47711", "Retail sale of clothing for adults"),
            ("47410", "Retail sale of computers, peripheral equipment and software in specialised stores"),
        ],
        "challenges": [
            ("GST registration timing", "Once your trailing 12-month turnover exceeds S$1M you have 30 days to register for GST. Voluntary registration earlier lets you claim back input GST on Singapore expenses but adds quarterly filing overhead."),
            ("Inventory accounting", "If you hold inventory, accounting becomes meaningfully more complex (COGS, write-downs, stock takes). Most pure dropship brands stay on cash basis; brands holding stock need accrual accounting from year one."),
            ("Stripe and acquirer due diligence", "Stripe and other gateways require a real business address, UEN, and bank account before activating. Some brands hit higher reserves until 90-day chargeback history is established."),
            ("Customs and BOM for physical goods", "Importing into Singapore requires HS code classification and the right BizFile activity codes. Most consumer goods are duty-free into Singapore but GST applies on imports if you're GST-registered."),
        ],
        "faqs": [
            ("Do I need GST registration as a Singapore e-commerce business?",
             "Mandatory once your trailing 12-month turnover from Singapore-taxable sales exceeds S$1M. Voluntary registration is allowed at any turnover and lets you claim back input GST on your Singapore costs. If 100% of your sales are exports (non-Singapore), they are zero-rated - you charge 0% GST but still register and claim refunds."),
            ("Can I run a Shopify store from a Singapore Pte Ltd?",
             "Yes. Shopify Singapore connects directly to Stripe Singapore, GrabPay, NETS, Atome, and other regional payment methods. You'll need a Singapore UEN, bank account, and GST registration (if applicable) to fully configure tax settings and payouts."),
            ("How does Singapore tax e-commerce sales to overseas customers?",
             "Income is taxed at the Singapore corporate rate (17%, with Startup Tax Exemption for first 3 years). GST is 0% on exports of goods. If you're a digital service seller (downloads, subscriptions) selling to non-business customers in Singapore, you may need to register for GST under the Overseas Vendor Regime once thresholds are met."),
            ("What's the best bank account for an e-commerce business?",
             "For multi-currency settlement: Wise Business or Aspire. For relationship banking once volume is high: DBS or OCBC. Aspire and Wise can be opened remotely in 3–5 days; DBS typically requires a Singapore visit. Stripe Singapore can settle to any of these in SGD."),
            ("Do I need a corporate secretary if I'm a small e-commerce brand?",
             "Yes - every Singapore Pte Ltd must appoint a qualified corporate secretary within 6 months of incorporation, regardless of revenue. Karman provides corporate secretary services from S$480/year covering AGM, annual return filing, and ACRA compliance."),
        ],
        "related": [
            ("tool", "/tools/cost-calculator", "Cost Calculator", "Estimate setup, secretary, accounting, and GST filing fees."),
            ("tool", "/tools/ssic-code-search", "SSIC Code Search", "Find the right activity code for your product category."),
            ("tool", "/tools/document-checklist", "Document Checklist", "All KYC and corporate documents you'll need."),
            ("template", "/templates/share-allotment", "Share Allotment Resolution", "Issue shares to early angels or co-founders."),
            ("template", "/templates/board-resolution", "Board Resolution", "Authorize bank account opening and payment processor setup."),
            ("term", "/glossary/gst", "Glossary: GST", "Singapore's 9% goods and services tax explained."),
            ("term", "/glossary/uen", "Glossary: UEN", "Your unique entity number - required for everything."),
            ("term", "/glossary/corporate-secretary", "Glossary: Corporate Secretary", "Why every Pte Ltd needs one within 6 months."),
        ],
    },
    {
        "slug": "saas",
        "name": "SaaS",
        "icon": "S",
        "title": "Singapore Incorporation for SaaS Companies | Karman",
        "description": "Incorporate a Singapore Pte Ltd for your SaaS business. Stripe, recurring revenue, GST on digital services, R&D credits, EP for engineering team. From S$699.",
        "hero_h1": "Singapore incorporation for SaaS and software companies",
        "hero_lede": "Bill globally in USD, defer R&D costs, and serve the world from a Pte Ltd that VCs and acquirers understand. Karman sets it up, files your annual return, and handles GST on digital services.",
        "answer": "<strong>SaaS companies typically incorporate as a Singapore Pte Ltd</strong> with a single class of ordinary shares, ESOP pool reserved, and a clean cap table for SAFE/convertible rounds. Singapore taxes SaaS revenue at 17% with a 75% exemption on the first S$100K for the first 3 years. Stripe Singapore handles global billing in 135+ currencies. Setup is 1–3 business days through ACRA.",
        "why_singapore": [
            ("Globally recognized cap table", "Standard Singapore Pte Ltd cap tables work cleanly with SAFE notes, convertibles, and priced rounds. US, UK, Indian, and Asia-focused investors all transact on Singapore docs without friction."),
            ("Recurring revenue infrastructure", "Stripe Billing, Chargebee, Paddle, and Maxio all support Singapore entities. Stripe Singapore settles to local SGD/USD accounts in 2 business days."),
            ("R&D super-deduction", "Up to 250% deduction on qualifying R&D activities under Section 14C/14D. Software development, ML, and product engineering generally qualify with the right documentation."),
            ("Talent and tax for engineers", "Employment Pass for senior hires, Tech.Pass for sponsor-free senior tech roles, and personal income tax that tops out at 24% - meaningfully lower than US, UK, India, or AU equivalents."),
        ],
        "structure_recipe": [
            ("Entity", "Singapore Pte Ltd"),
            ("Share capital", "S$1 paid-up minimum; common splits: founders 80–90%, ESOP pool 10–15%, advisors 1–3%"),
            ("Cap table", "Single class ordinary shares; SAFE/convertible-friendly; preference shares introduced at priced rounds"),
            ("Directors", "≥1 ordinary resident director"),
            ("Bank", "Aspire or Wise Business for global billing; DBS for relationship banking at scale"),
            ("Billing", "Stripe Billing (default), Chargebee for complex pricing, Paddle for merchant-of-record handling of EU VAT"),
        ],
        "ssic_codes": [
            ("62019", "Development of other software and programming activities"),
            ("62029", "Other information technology and computer service activities"),
            ("63111", "Data processing, hosting and related activities"),
            ("58202", "Publishing of software (except games)"),
        ],
        "challenges": [
            ("GST on digital services", "Under Singapore's Overseas Vendor Regime, you may need to register and charge GST to Singapore B2C customers once thresholds are met (S$1M global turnover and S$100K of B2C Singapore sales). B2B customers are zero-rated under reverse charge."),
            ("EU VAT on subscriptions", "If you sell to EU consumers, you may need EU VAT registration (or use a merchant-of-record like Paddle that handles it for you). Stripe Tax automates VAT handling once configured."),
            ("ESOP design", "Singapore ESOPs are flexible. Most SaaS companies use a 4-year vesting with 1-year cliff, exercise window of 90 days post-departure, and a separate ESOP trust if cap table cleanliness matters for fundraising."),
            ("Recognising deferred revenue", "ARR/MRR-driven businesses must defer revenue across the subscription period. This requires accrual-basis accounting from day one - Karman's accounting service handles deferred revenue, churn, and SaaS-specific reporting."),
        ],
        "faqs": [
            ("Should a SaaS startup incorporate in Singapore or Delaware?",
             "If your investors are primarily US (Sequoia US, a16z, YC alumni-led funds), Delaware C-Corp is still the path of least resistance. If you're raising from Asia-focused VCs, serving Asia customers, or wanting lower tax friction at scale, Singapore Pte Ltd is the better default. Many founders dual-structure (Cayman parent + Singapore operating subsidiary) to satisfy US fund requirements while operating from Singapore."),
            ("Do I need to charge GST on SaaS subscriptions?",
             "Depends on the customer's location and your turnover. To Singapore B2C customers: yes, once you cross OVR thresholds. To Singapore B2B customers: zero-rated under reverse charge. To non-Singapore customers: zero-rated as exports. Stripe Tax automates this once you've configured your registrations."),
            ("How does Singapore handle SaaS revenue recognition for tax?",
             "You're taxed on accrued profit, not cash receipts. If you bill annually upfront for a 12-month subscription, you recognise 1/12 of the revenue per month. Your tax return reflects accrued income, so deferred revenue reduces taxable profit until earned."),
            ("Can I claim R&D credits on SaaS product development?",
             "Yes - qualifying activities under Section 14C/14D include software development that solves technical uncertainty (new architectures, algorithms, novel integrations). Routine bug fixes and UI work generally don't qualify. You need contemporaneous documentation: project descriptions, time-tracking, and outcomes. Karman's accounting team can help structure your R&D claims."),
            ("What's the right legal structure for ESOP grants?",
             "Most Singapore SaaS startups grant share options (not RSUs) under a board-approved ESOP plan. Reserve a 10–15% pool at incorporation, document it in a board resolution, and grant from the pool as you hire. Karman provides the board resolution template and corporate secretary support to record each grant."),
        ],
        "related": [
            ("tool", "/tools/business-structure-recommender", "Structure Recommender", "Pte Ltd, Cayman parent, or LLC - get the right answer."),
            ("tool", "/tools/cost-calculator", "Cost Calculator", "Estimate annual ongoing costs at your scale."),
            ("tool", "/tools/eligibility-checker", "Eligibility Checker", "Check what you need as a foreign-founded SaaS."),
            ("template", "/templates/founders-agreement", "Founders' Agreement", "Equity splits, vesting, IP assignment, and exit terms."),
            ("template", "/templates/share-allotment", "Share Allotment Resolution", "Issue shares to angels, advisors, and ESOP grantees."),
            ("term", "/glossary/pte-ltd", "Glossary: Pte Ltd", "What a private limited company is and isn't."),
            ("term", "/glossary/share-capital", "Glossary: Share Capital", "How share capital works in Singapore."),
            ("term", "/glossary/corporate-tax", "Glossary: Corporate Tax", "17% headline rate and the exemptions that lower it."),
        ],
    },
    {
        "slug": "fintech",
        "name": "Fintech",
        "icon": "F",
        "title": "Singapore Incorporation for Fintech Companies | Karman",
        "description": "Incorporate a Singapore Pte Ltd for your fintech business. MAS Payment Services Act licensing, capital markets services, regulatory sandbox guidance. From S$699.",
        "hero_h1": "Singapore incorporation for fintech and payment companies",
        "hero_lede": "Singapore is the regulated fintech capital of Asia. We handle the Pte Ltd incorporation; we'll point you to the right MAS licensing pathway (PSA, CMS, sandbox) before you raise.",
        "answer": "<strong>Most fintechs incorporate a Singapore Pte Ltd first, then apply to MAS for the relevant licence.</strong> The Payment Services Act (PSA) covers most payment, e-money, and digital token activities. Capital Markets Services (CMS) licence covers wealth, brokerage, and fund management. The Regulatory Sandbox lets you test live for up to 12 months under relaxed conditions. Incorporation is 1–3 business days; licensing is 4–12 months depending on activity.",
        "why_singapore": [
            ("MAS - a regulator that engages", "MAS publishes clear guidance, runs an active fintech office, and engages with founders pre-application. The Sandbox and Sandbox Express let you test live with relaxed requirements while applying for full licensing."),
            ("Predictable licensing pathways", "PSA covers payment services, e-money, digital tokens, cross-border money transfer, and merchant acquisition. CMS covers fund management, dealing in capital markets products. Each activity has a defined application path."),
            ("Capital and talent gravity", "Singapore concentrates more fintech VC dry powder than any other Asia hub. Tech.Pass, ONE Pass, and EP routes for senior compliance, risk, and engineering talent."),
            ("Tax incentives at scale", "Financial Sector Incentive (FSI) schemes can lower tax on qualifying activities to 5%, 10%, or 13.5%. Section 13O and 13U cover funds. Most fintechs benefit from the standard 17% with Startup Tax Exemption first."),
        ],
        "structure_recipe": [
            ("Entity", "Singapore Pte Ltd (mandatory for MAS-licensed activities)"),
            ("Share capital", "S$1 to incorporate; PSA Standard Payment Institution requires S$100K base capital, Major Payment Institution requires S$250K"),
            ("Directors", "≥1 ordinary resident director; for MAS-licensed entities, fit-and-proper test applies to all directors and key officers"),
            ("Compliance", "Compliance officer (often part-time outsourced for early stage), AML/CFT framework, transaction monitoring"),
            ("Bank", "DBS or OCBC strongly preferred for licensed entities; Aspire and Wise can work pre-licensing"),
            ("Pre-licensing", "Engage MAS via fintech office; consider Sandbox Express for narrowly-defined live tests"),
        ],
        "ssic_codes": [
            ("64999", "Other financial service activities, n.e.c. (e.g., fintech)"),
            ("66199", "Other activities auxiliary to financial service activities n.e.c."),
            ("64202", "Holding companies (financial holding companies)"),
            ("62019", "Development of other software and programming activities"),
        ],
        "challenges": [
            ("Picking the right MAS licence", "Activities map to specific licences: account issuance → e-money issuance under PSA; cross-border remittance → cross-border money transfer service under PSA; fund management → CMS licence. Don't incorporate before you've identified the licence - capital and structuring requirements differ."),
            ("Capital lock-in", "PSA Standard Payment Institution requires S$100K base capital that must remain ring-fenced; Major Payment Institution requires S$250K. CMS capital ranges from S$250K to S$5M depending on activity. Karman flags this before you fund."),
            ("Compliance and AML overhead", "Licensed fintechs need an AML/CFT framework, transaction monitoring, periodic reporting, and at least one nominated compliance officer. Plan for S$60K–S$200K/year of compliance overhead even at early stage."),
            ("Bank account opening for licensed entities", "DBS, OCBC, and UOB are the practical options for MAS-licensed fintechs. Account opening can take 4–8 weeks and requires a clean licence and clean source-of-funds documentation."),
        ],
        "faqs": [
            ("Do I need a MAS licence to incorporate a fintech in Singapore?",
             "No - you can incorporate a Pte Ltd without any licence. You only need a MAS licence to actually carry on a regulated activity (payment services, fund management, capital markets dealing, etc.). Many fintechs incorporate first, build a prototype, then apply for the relevant licence with a working product. The Sandbox and Sandbox Express let you test live for limited periods under relaxed conditions."),
            ("Which MAS licence do I need?",
             "Depends on your activity. PSA covers payment services (account issuance, domestic transfers, cross-border transfers, e-money issuance, digital token services, merchant acquisition). CMS covers capital markets activities (fund management, dealing in securities, advising on corporate finance). Insurance broking has its own regime. We'll help you map your business model to the right licence pre-incorporation."),
            ("How long does MAS licensing take?",
             "PSA Standard Payment Institution: typically 4–6 months. PSA Major Payment Institution: 6–12 months. CMS: 6–12 months. Sandbox approvals can be faster (1–3 months) but are time-limited and scope-limited. The clock starts once MAS deems your application substantively complete - incomplete submissions add months."),
            ("How much capital do I need for a Payment Services licence?",
             "Standard Payment Institution: S$100K base capital. Major Payment Institution: S$250K. Money-Changing licence: S$100K. Capital must be unimpaired and ring-fenced. There are also security deposit requirements for cross-border money transfer. Karman's fintech onboarding flow walks you through capital structuring before you fund."),
            ("Can I do crypto in Singapore?",
             "Digital Token Service Providers (DTSPs) are regulated under the PSA. As of 2026, MAS has tightened the regime for crypto firms serving overseas customers from Singapore - the bar for licensing has risen substantially. Realistic assessment: only well-capitalised, compliance-mature crypto businesses get licensed. We can advise on whether your model is viable before you incorporate."),
        ],
        "related": [
            ("tool", "/tools/business-structure-recommender", "Structure Recommender", "Confirm Pte Ltd is right for your fintech model."),
            ("tool", "/tools/cost-calculator", "Cost Calculator", "Estimate annual fees including MAS-related compliance overhead."),
            ("tool", "/tools/eligibility-checker", "Eligibility Checker", "Check incorporation eligibility for foreign founders."),
            ("template", "/templates/board-resolution", "Board Resolution", "Required for bank account opening and licence applications."),
            ("template", "/templates/founders-agreement", "Founders' Agreement", "Equity, vesting, and IP - the cleaner the cap table the easier MAS fit-and-proper review."),
            ("term", "/glossary/pte-ltd", "Glossary: Pte Ltd", "Why Pte Ltd is mandatory for MAS-regulated activities."),
            ("term", "/glossary/section-13o", "Glossary: Section 13O", "Fund tax incentive (relevant for wealth fintechs)."),
            ("term", "/glossary/vcc", "Glossary: VCC", "Variable Capital Company - used by fund-management fintechs."),
        ],
    },
    {
        "slug": "crypto",
        "name": "Web3 & Crypto",
        "icon": "C",
        "title": "Singapore Incorporation for Web3 and Crypto Companies | Karman",
        "description": "Incorporate a Singapore Pte Ltd for your Web3 or crypto business. DTSP licensing under PSA, MAS sandbox, foundation vs Pte Ltd structuring. From S$699.",
        "hero_h1": "Singapore incorporation for Web3 and crypto companies",
        "hero_lede": "Singapore remains the most credible jurisdiction in Asia for compliant crypto businesses - but the bar has risen. We help you incorporate the right entity (Pte Ltd, Foundation, or both) and prepare for MAS licensing before you go live.",
        "answer": "<strong>Web3 companies typically incorporate a Singapore Pte Ltd</strong>, with token-issuance entities sometimes structured as a foundation (Cayman or BVI) for governance reasons. Digital Token Service Provider (DTSP) activities require a MAS licence under the Payment Services Act. As of 2026, MAS has materially tightened the bar for licensing - early honest assessment of viability is critical before incorporating.",
        "why_singapore": [
            ("Regulator clarity", "MAS publishes detailed guidance on what constitutes a Digital Payment Token, when DTSP licensing applies, and what the fit-and-proper bar looks like. Few jurisdictions are as transparent."),
            ("Banking access for licensed entities", "DBS, OCBC, and StraitsX serve compliant licensed crypto entities. Pre-licensing, banking is harder - most early-stage entities use Aspire or operate via stablecoin custodians."),
            ("Talent and ecosystem", "Singapore has dense Web3 talent (engineers, lawyers, compliance, market makers). Token2049, ETH Singapore, and a dozen accelerator programs run from Singapore."),
            ("Token-economics-friendly tax treatment", "Singapore does not tax capital gains. Token sales by a Singapore Pte Ltd may be treated as either trading (taxable income) or capital (non-taxable) depending on facts. IRAS publishes specific guidance for digital tokens."),
        ],
        "structure_recipe": [
            ("Entity", "Singapore Pte Ltd for the operating company; Cayman or BVI Foundation for the token-issuing entity (optional)"),
            ("Share capital", "S$1 to incorporate; if applying for DTSP licence, MAS will assess capital adequacy on a case-by-case basis (often S$250K+)"),
            ("Directors", "≥1 ordinary resident director; fit-and-proper applies to all directors and key officers if licensed"),
            ("Compliance", "Travel Rule compliance, AML/CFT framework, KYC, sanctions screening, transaction monitoring"),
            ("Bank", "Pre-licensing: Aspire, Wise, or stablecoin treasury via Fireblocks/StraitsX. Post-licensing: DBS or OCBC (still difficult)"),
            ("Token issuance", "Often via a separate Foundation (Cayman/BVI) with the Singapore Pte Ltd as service provider - get legal advice on structuring before issuing"),
        ],
        "ssic_codes": [
            ("64999", "Other financial service activities, n.e.c."),
            ("62019", "Development of other software and programming activities"),
            ("66199", "Other activities auxiliary to financial service activities n.e.c."),
            ("63111", "Data processing, hosting and related activities"),
        ],
        "challenges": [
            ("DTSP licensing bar has risen", "As of 2026, MAS has tightened DTSP requirements for entities serving non-Singapore customers from Singapore. Realistic assessment: only well-capitalised, compliance-mature entities get licensed. Don't incorporate before honest viability assessment."),
            ("Banking is the binding constraint", "Local banks remain cautious on crypto exposure. Pre-licensing, plan for stablecoin treasury and limited fiat rails. Post-licensing, banking opens up but is still slow - expect 3–6 months and detailed source-of-funds review."),
            ("Token tax treatment", "IRAS distinguishes payment tokens, utility tokens, and security tokens - each treated differently. Token sales may be capital (untaxed) or trading (17% corporate tax). Get an early opinion before your first issuance."),
            ("Foundation vs Pte Ltd structuring", "Many Web3 projects use a Cayman/BVI Foundation as the token issuer (decentralised governance) with a Singapore Pte Ltd as service provider. This is a structuring decision with tax, securities, and governance implications - get specialist advice."),
        ],
        "faqs": [
            ("Can I run a crypto exchange from Singapore?",
             "Yes, if you obtain a Digital Token Service Provider licence under the Payment Services Act. As of 2026, MAS has tightened the bar materially - only well-capitalised, compliance-mature businesses get licensed. Operating without a licence carries criminal penalties. The Sandbox is not available for crypto exchange activities."),
            ("Do I need a MAS licence to issue a token from Singapore?",
             "Depends on the token. If it is a Digital Payment Token (intended as payment), DTSP licensing applies. If it is a Securities Token (capital markets product), CMS licensing and prospectus rules apply. Pure utility tokens issued by a foreign foundation with no Singapore solicitation may sit outside MAS perimeter - but the analysis is fact-specific. Get a legal opinion before issuance."),
            ("Should I use a Cayman Foundation or Singapore Pte Ltd for my token?",
             "Most decentralised projects use a Cayman or BVI Foundation as the token issuer (for ownerless governance and tax neutrality), with a Singapore Pte Ltd as the development and service-provider entity. Centralised products often issue directly from a Singapore Pte Ltd. The right answer depends on your token model, investor expectations, and regulatory perimeter."),
            ("Are crypto gains taxed in Singapore?",
             "Singapore does not tax capital gains. If your trading in crypto is held as a long-term investment, gains are typically not taxed. If you trade frequently or treat it as a business activity, profits may be taxed at the 17% corporate rate. IRAS publishes a specific e-Tax Guide on Digital Tokens - read it before structuring."),
            ("Can foreign founders incorporate a Web3 Pte Ltd remotely?",
             "Yes - incorporation itself is fully remote. KYC is conducted by your filing agent. You'll need at least one ordinary resident director (Karman provides nominee director services from S$2,400/year while you secure your own EP). Banking and licensing typically require a Singapore visit at later stages."),
        ],
        "related": [
            ("tool", "/tools/business-structure-recommender", "Structure Recommender", "Pte Ltd, Foundation, or both - get clarity."),
            ("tool", "/tools/cost-calculator", "Cost Calculator", "Estimate setup, ongoing, and compliance overhead."),
            ("tool", "/tools/eligibility-checker", "Eligibility Checker", "Check if you can incorporate as a foreign founder."),
            ("template", "/templates/founders-agreement", "Founders' Agreement", "Equity, vesting, IP, and token allocation alignment."),
            ("template", "/templates/mutual-nda", "Mutual NDA", "Protect protocol designs, treasury structures, and partner discussions."),
            ("term", "/glossary/pte-ltd", "Glossary: Pte Ltd", "Why Pte Ltd is the operating-company default."),
            ("term", "/glossary/corporate-tax", "Glossary: Corporate Tax", "How Singapore's 17% rate applies to crypto trading vs holding."),
            ("term", "/glossary/kyc", "Glossary: KYC", "What MAS expects for fit-and-proper review."),
        ],
    },
]


def esc(s):
    return htmlmod.escape(s, quote=True) if s else ""


def page_head(title, description, canonical_path, ldjson):
    return f"""<!DOCTYPE html>
<html lang="en-SG">
<head>
  <!-- Google tag (gtag.js) -->
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', 'G-DVKN5K8KSD');
    function loadGTM(){{
      if (window.__gtmLoaded) return;
      window.__gtmLoaded = true;
      var s = document.createElement('script');
      s.async = true;
      s.src = 'https://www.googletagmanager.com/gtag/js?id=G-DVKN5K8KSD';
      document.head.appendChild(s);
    }}
    if ('requestIdleCallback' in window) {{
      requestIdleCallback(loadGTM, {{timeout: 3000}});
    }} else {{
      window.addEventListener('load', function(){{ setTimeout(loadGTM, 1500); }});
    }}
  </script>

  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <link rel="icon" type="image/png" href="/favicon.png" />
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(description)}" />
  <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1" />
  <meta name="author" content="Karman Corporate Services Pte Ltd" />
  <link rel="canonical" href="https://karman.com.sg{canonical_path}" />

  <meta name="geo.region" content="SG" />
  <meta name="geo.placename" content="Singapore" />

  <meta property="og:type" content="website" />
  <meta property="og:url" content="https://karman.com.sg{canonical_path}" />
  <meta property="og:site_name" content="Karman Corporate Services" />
  <meta property="og:title" content="{esc(title)}" />
  <meta property="og:description" content="{esc(description)}" />
  <meta property="og:image" content="https://karman.com.sg/logo.png" />
  <meta property="og:locale" content="en_SG" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{esc(title)}" />
  <meta name="twitter:description" content="{esc(description)}" />
  <meta name="twitter:image" content="https://karman.com.sg/logo.png" />
  <meta name="theme-color" content="#0A2540" />

  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Sora:wght@400;600;700;800&display=swap" />
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Sora:wght@400;600;700;800&display=swap" media="print" onload="this.media='all'" />
  <noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Sora:wght@400;600;700;800&display=swap" /></noscript>
  <link rel="stylesheet" href="/styles.css" />

  <script type="application/ld+json">
{json.dumps(ldjson, ensure_ascii=False, indent=2)}
  </script>

  <style>
{CSS}  </style>
</head>
<body>

{NAV_HTML}"""


def industry_ldjson(ind):
    canonical = f"https://karman.com.sg/for/{ind['slug']}"
    return {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebPage",
                "@id": f"{canonical}#webpage",
                "url": canonical,
                "name": ind["title"],
                "description": ind["description"],
                "inLanguage": "en-SG",
                "isPartOf": {"@id": "https://karman.com.sg#website"},
                "speakable": {
                    "@type": "SpeakableSpecification",
                    "cssSelector": ["h1", ".ind-answer", ".ind-faq summary"],
                },
                "primaryImageOfPage": {"@type": "ImageObject", "url": "https://karman.com.sg/logo.png"},
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://karman.com.sg/"},
                    {"@type": "ListItem", "position": 2, "name": "Industries", "item": "https://karman.com.sg/for"},
                    {"@type": "ListItem", "position": 3, "name": ind["name"], "item": canonical},
                ],
            },
            {
                "@type": "FAQPage",
                "@id": f"{canonical}#faq",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": a},
                    }
                    for (q, a) in ind["faqs"]
                ],
            },
        ],
    }


def hub_ldjson():
    canonical = "https://karman.com.sg/for"
    return {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "CollectionPage",
                "@id": f"{canonical}#webpage",
                "url": canonical,
                "name": "Industry guides for Singapore incorporation",
                "description": "Singapore Pte Ltd incorporation guides by industry: AI startups, e-commerce, SaaS, fintech, and Web3.",
                "inLanguage": "en-SG",
                "speakable": {"@type": "SpeakableSpecification", "cssSelector": ["h1", ".ind-hub__lede"]},
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://karman.com.sg/"},
                    {"@type": "ListItem", "position": 2, "name": "Industries", "item": canonical},
                ],
            },
        ],
    }


RELATED_LABELS = {"tool": "Free tool", "template": "Template", "term": "Glossary"}


def render_industry(ind):
    canonical_path = f"/for/{ind['slug']}"
    ld = industry_ldjson(ind)

    why_cards = "\n".join(
        f'        <div class="ind-card"><h3>{esc(t)}</h3><p>{esc(d)}</p></div>'
        for (t, d) in ind["why_singapore"]
    )

    recipe_items = "\n".join(
        f'          <li><strong>{esc(k)}</strong><span>{esc(v)}</span></li>'
        for (k, v) in ind["structure_recipe"]
    )

    ssic_chips = "\n".join(
        f'        <a href="/tools/ssic-code-search?q={code}"><code>{code}</code> <span>{esc(desc)}</span></a>'
        for (code, desc) in ind["ssic_codes"]
    )

    challenge_items = "\n".join(
        f'        <div class="ind-stack__item"><h3>{esc(t)}</h3><p>{esc(d)}</p></div>'
        for (t, d) in ind["challenges"]
    )

    faq_items = "\n".join(
        f'        <details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>'
        for (q, a) in ind["faqs"]
    )

    related_cards = "\n".join(
        f'        <a href="{esc(href)}"><span class="ind-related__label">{RELATED_LABELS[kind]}</span><div class="ind-related__title">{esc(title)}</div><p class="ind-related__desc">{esc(desc)}</p></a>'
        for (kind, href, title, desc) in ind["related"]
    )

    body = f"""
  <main>
    <section class="ind-hero">
      <div class="container">
        <nav class="ind-hero__breadcrumb" aria-label="Breadcrumb">
          <a href="/">Home</a><span>›</span>
          <a href="/for">Industries</a><span>›</span>
          <span>{esc(ind['name'])}</span>
        </nav>
        <span class="ind-hero__pill">For {esc(ind['name'])}</span>
        <h1>{esc(ind['hero_h1'])}</h1>
        <p class="ind-hero__lede">{esc(ind['hero_lede'])}</p>
        <div class="ind-answer"><p>{ind['answer']}</p></div>
        <div class="ind-hero__cta">
          <a href="/#get-started" class="btn btn--primary">Get started - S$699</a>
          <a href="/#contact" class="btn btn--secondary">Talk to us first</a>
        </div>
      </div>
    </section>

    <section class="ind-section">
      <div class="container">
        <h2>Why founders choose Singapore for {esc(ind['name'].lower())}</h2>
        <div class="ind-grid">
{why_cards}
        </div>
      </div>
    </section>

    <section class="ind-section ind-section--gray">
      <div class="container">
        <h2>The recommended structure</h2>
        <p class="ind-section__sub">A typical {esc(ind['name'])} setup. Specific choices depend on your investors, jurisdictions you serve, and exit plans.</p>
        <div class="ind-recipe">
          <h3>Default {esc(ind['name'])} stack</h3>
          <ul>
{recipe_items}
          </ul>
        </div>
      </div>
    </section>

    <section class="ind-section">
      <div class="container">
        <h2>Common SSIC codes</h2>
        <p class="ind-section__sub">SSIC 2020 codes most often used at incorporation. Click any code to look it up in our search tool.</p>
        <div class="ind-ssic">
{ssic_chips}
        </div>
      </div>
    </section>

    <section class="ind-section ind-section--gray">
      <div class="container">
        <h2>What to plan for</h2>
        <p class="ind-section__sub">The four things that most often surprise {esc(ind['name'])} founders setting up in Singapore.</p>
        <div class="ind-stack">
{challenge_items}
        </div>
      </div>
    </section>

    <section class="ind-section">
      <div class="container">
        <h2>Frequently asked questions</h2>
        <div class="ind-faq">
{faq_items}
        </div>
      </div>
    </section>

    <section class="ind-section ind-section--gray">
      <div class="container">
        <h2>Related Karman tools, templates, and definitions</h2>
        <p class="ind-section__sub">Free resources to plan your {esc(ind['name'])} setup.</p>
        <div class="ind-related">
{related_cards}
        </div>
      </div>
    </section>

    <section class="ind-section">
      <div class="container">
        <div class="ind-cta">
          <h2>Ready to set up your {esc(ind['name'])} entity?</h2>
          <p>Karman is an ACRA-registered filing agent. We handle incorporation, corporate secretary, accounting, GST, and EP applications - all in one place. Most {esc(ind['name'])} founders are operational within 2 weeks.</p>
          <a href="/#get-started" class="btn">Start incorporation</a>
        </div>
      </div>
    </section>
  </main>

{FOOTER_HTML}
  <script src="/script.js"></script>
</body>
</html>
"""

    return page_head(ind["title"], ind["description"], canonical_path, ld) + body


def render_hub():
    canonical_path = "/for"
    ld = hub_ldjson()

    cards = "\n".join(
        f'        <a class="ind-hub__card" href="/for/{ind["slug"]}"><div class="ind-hub__card-icon">{ind["icon"]}</div><h3>{esc(ind["name"])}</h3><p>{esc(ind["description"])}</p><div class="ind-hub__card-cta">Read the guide →</div></a>'
        for ind in INDUSTRIES
    )

    body = f"""
  <main>
    <section class="ind-hub">
      <div class="container">
        <nav class="ind-hero__breadcrumb" aria-label="Breadcrumb">
          <a href="/">Home</a><span>›</span>
          <span>Industries</span>
        </nav>
        <h1>Singapore incorporation guides by industry</h1>
        <p class="ind-hub__lede">Industry-specific Pte Ltd setup playbooks. Each guide covers the recommended structure, SSIC codes, common challenges, MAS or sector-specific licensing, and the templates and tools that apply.</p>
        <div class="ind-hub__grid">
{cards}
        </div>
      </div>
    </section>
  </main>

{FOOTER_HTML}
  <script src="/script.js"></script>
</body>
</html>
"""

    title = "Singapore Incorporation Guides by Industry | Karman"
    description = "Industry-specific Singapore incorporation playbooks for AI startups, e-commerce brands, SaaS, fintech, and Web3 founders."
    return page_head(title, description, canonical_path, ld) + body


def main():
    OUT_DIR.mkdir(exist_ok=True)
    (OUT_DIR / "index.html").write_text(render_hub(), encoding="utf-8")
    print(f"Wrote {OUT_DIR / 'index.html'}")
    for ind in INDUSTRIES:
        d = OUT_DIR / ind["slug"]
        d.mkdir(exist_ok=True)
        (d / "index.html").write_text(render_industry(ind), encoding="utf-8")
        print(f"Wrote {d / 'index.html'}")


if __name__ == "__main__":
    main()
