#!/usr/bin/env python3
"""Generate 5 priority blog posts under /blog/<slug>/index.html."""

import json
import html as htmlmod
from pathlib import Path
STYLES_CSS_INLINE = (Path(__file__).resolve().parent.parent / "styles.css").read_text(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
BLOG_DIR = ROOT / "blog"

PUB_DATE = "2026-05-07"
READ_TIMES = {  # populated per blog
}


def esc(s):
    return htmlmod.escape(s, quote=True) if s else ""


HEADER_HTML = """  <header class="header" id="header">
    <nav class="nav container" aria-label="Main navigation">
      <a href="/" class="nav__logo"><img src="/logo.svg" alt="Karman" class="nav__logo-img" width="124" height="40" fetchpriority="high"></a>
      <ul class="nav__menu" id="navMenu">
        <li class="nav__item"><a href="/#services" class="nav__link">Services</a></li>
        <li class="nav__item"><a href="/about" class="nav__link">About</a></li>
        <li class="nav__item"><a href="/tools" class="nav__link">Free Tools <span class="nav__badge">Free</span></a></li>
        <li class="nav__item"><a href="/blog" class="nav__link nav__link--active">Blog</a></li>
        <li class="nav__item"><a href="/faq" class="nav__link">FAQ</a></li>
      </ul>
      <div class="nav__actions">
        <a href="/#contact" class="btn btn--secondary">Contact us</a>
        <a href="/onboarding" class="btn btn--primary">Get started</a>
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
          <div class="footer-col"><h4>Services</h4><ul>
            <li><a href="/#incorporation">Company Incorporation</a></li>
            <li><a href="/services/vcc-fund-administration">VCC &amp; Fund Administration</a></li>
            <li><a href="/#secretary">Corporate Secretarial</a></li>
            <li><a href="/#accounting">Accounting &amp; Bookkeeping</a></li>
          </ul></div>
          <div class="footer-col"><h4>Resources</h4><ul>
            <li><a href="/tools">Free Tools</a></li>
            <li><a href="/templates/">Templates</a></li>
            <li><a href="/glossary/">Glossary</a></li>
            <li><a href="/for">Industry Guides</a></li>
            <li><a href="/blog">Blog</a></li>
            <li><a href="/#faq">FAQ</a></li>
          </ul></div>
          <div class="footer-col"><h4>Company</h4><ul>
            <li><a href="/#about">About Karman</a></li>
            <li><a href="/#contact">Contact</a></li>
          </ul></div>
        </div>
      </div>
      <div class="footer__bottom">
        <p>© 2026 Karman Corporate Services Pte Ltd. UEN: 202012889R. 60 Paya Lebar Road, #06-28, Paya Lebar Square, Singapore 409051</p>
      </div>
    </div>
  </footer>
"""


# ============================================================================
# BLOG DATA
# ============================================================================

BLOGS = [
    # ------------------------------------------------------------------
    # 1. InvoiceNow GST mandate
    # ------------------------------------------------------------------
    {
        "slug": "gst-invoicenow-singapore-2026",
        "title": "GST InvoiceNow Singapore: 2026 Rollout & Founder Action Plan",
        "description": "From 1 April 2026 all newly GST-registered Singapore companies must use InvoiceNow. Full mandate by 2031. Here's what founders must do, when, and how.",
        "keyword": "gst invoicenow singapore 2026",
        "tag": "GST",
        "tag_class": "gst",
        "breadcrumb_short": "InvoiceNow GST 2026",
        "read_min": 9,
        "lede": "From 1 April 2026, all <strong>newly GST-registered companies</strong> in Singapore must transmit invoice data to IRAS via the InvoiceNow network. By 2031, this becomes mandatory for every GST-registered business in Singapore. If you incorporate now and plan to register for GST - voluntarily or once you cross S$1M turnover - this affects you. Here's what to do, when to do it, and what it costs.",
        "intro_p2": "InvoiceNow is Singapore's nationwide e-invoicing network, built on the Peppol standard. It lets businesses send invoices directly between accounting systems - no PDFs, no emails, no manual data entry. From April 2026 onwards, IRAS uses this network to receive invoice data in real time as part of GST filing.",
        "sections": [
            ("What is InvoiceNow, exactly?",
             [
                 "InvoiceNow is the Singapore brand for the international Peppol e-invoicing network. Peppol is a global standard that lets a sending system in Singapore deliver a structured invoice directly to a receiving system anywhere on the network - including buyers in Australia, the EU, Japan, Malaysia, and other Peppol-enabled jurisdictions.",
                 "Think of it like email for invoices: instead of attaching a PDF and hoping the recipient types the numbers correctly into their system, the data flows in machine-readable form from your accounting software to theirs.",
                 "<strong>Why Singapore is mandating it for GST:</strong> IRAS gets near-real-time visibility into invoice flows. Instead of relying on companies to summarise transactions quarterly in their GST F5 return, IRAS receives the data as it happens. This reduces fraud, automates GST refund verification, and lets the agency move toward continuous compliance rather than annual audit cycles.",
             ]),
            ("The phased timeline (2026 to 2031)",
             [
                 "IRAS is rolling out the InvoiceNow GST requirement in three phases. Mark your calendar based on when you incorporate and when you register for GST.",
                 '<div class="callout callout--teal"><div class="callout__title">Phase 1 - 1 May 2025 (already live)</div><p>Voluntary early adoption open to all GST-registered companies. Businesses that adopt early get IRAS support and certain compliance reliefs.</p></div>',
                 '<div class="callout callout--amber"><div class="callout__title">Phase 2 - 1 November 2025</div><p>Mandatory for all newly incorporated companies that voluntarily register for GST. If you incorporated after this date and choose voluntary GST registration, you must use InvoiceNow.</p></div>',
                 '<div class="callout callout--teal"><div class="callout__title">Phase 3 - 1 April 2026 (the big one)</div><p>Mandatory for <strong>all</strong> newly GST-registered businesses, whether registration is voluntary or compulsory (after crossing S$1M turnover).</p></div>',
                 '<div class="callout"><div class="callout__title">Phase 4 - 2028 onwards</div><p>IRAS has signalled progressive expansion to existing GST-registered businesses, with full mandate by 2031. Exact dates per cohort will be confirmed closer to time.</p></div>',
             ]),
            ("Who is affected right now?",
             [
                 "If you fall into any of these categories, InvoiceNow GST applies to you:",
                 "<ul><li><strong>Newly incorporated and voluntarily registering for GST</strong> on or after 1 November 2025</li><li><strong>Any business newly registering for GST</strong> on or after 1 April 2026 (including compulsory registration after crossing S$1M turnover)</li><li><strong>Existing GST-registered businesses</strong> - not yet mandatory, but voluntary adoption is recommended given the 2028-2031 expansion</li></ul>",
                 "If you have an existing Singapore Pte Ltd that is already GST-registered, you have time. But if you incorporate today and plan to register for GST, you should plan for InvoiceNow from day one rather than retrofit later.",
             ]),
            ("What you actually need to do",
             [
                 "There are four practical steps to comply:",
                 "<ol><li><strong>Choose an InvoiceNow-ready accounting system or solution provider.</strong> Xero, Quickbooks Online, SAP Business One, Microsoft Dynamics, and most modern Singapore-friendly accounting systems are either already enabled or have InvoiceNow modules. Karman's accounting clients are migrated automatically.</li><li><strong>Get a Peppol ID (also called a Peppol Participant Identifier).</strong> Your accounting software or service provider issues this. It's how invoices route to your business on the Peppol network.</li><li><strong>Register your Peppol ID with IMDA's registry</strong> (the Infocomm Media Development Authority runs the Singapore Peppol Authority). This makes your business discoverable on the network.</li><li><strong>Configure transmission to IRAS for GST data.</strong> Your accounting system or solution provider handles this; it's a configuration setting, not a separate filing.</li></ol>",
                 "Once configured, your sales and purchase invoices flow into IRAS automatically. You still file your GST F5 return as normal, but the underlying transaction data is already with IRAS by the time you file - which means refund verification is much faster.",
             ]),
            ("Cost and time commitment",
             [
                 "<strong>Time to implement:</strong> 2-4 weeks for most small businesses. Most of this is configuration with your accounting system provider.",
                 "<strong>Direct cost:</strong> If you're already on a modern cloud accounting system (Xero, QBO), the InvoiceNow capability is typically included or available as a low-cost add-on (S$0-S$30/month). Some access-point providers charge per-invoice for high volumes.",
                 "<strong>Ongoing cost:</strong> Negligible if your invoice volume is under 1,000/month. Higher volume businesses may negotiate volume pricing with their access-point provider.",
                 "<strong>If you don't have accounting software yet:</strong> This is the moment to set one up. Trying to InvoiceNow-comply without a proper accounting system is far more painful than picking the right system from day one.",
             ]),
            ("What changes operationally",
             [
                 "Day-to-day, very little visible change for most founders. You still issue invoices the way you always have - through your accounting system. The difference is that the system silently transmits invoice data to IRAS in the background and to your customers (if they're also on Peppol) directly into their system.",
                 "<strong>What you'll notice:</strong>",
                 "<ul><li>Faster GST refunds when you're in a refund position</li><li>Fewer GST F5 reconciliation issues - IRAS already has the data</li><li>Less data entry friction with B2B customers who are on Peppol</li><li>More visibility for IRAS into your transactions (this is the trade-off)</li></ul>",
                 "<strong>What you don't have to do:</strong> You don't need to send invoices via Peppol to consumers (B2C). Retail receipts and consumer-facing invoices are out of scope for now. The mandate is for B2B and IRAS reporting.",
             ]),
            ("Should you adopt early (before April 2026)?",
             [
                 "If you're newly incorporated and plan to register for GST, the answer is straightforward: yes, set up InvoiceNow at the same time you set up your accounting system. The marginal effort is tiny when you're starting fresh.",
                 "If you're an existing GST-registered business not yet required to comply: voluntary adoption gives you a smoother transition window, IRAS implementation support, and time to fix any data quality issues before it becomes mandatory in 2028+. Most Karman accounting clients in this category are migrating in 2026 rather than waiting for the mandate.",
             ]),
            ("How Karman handles this for clients",
             [
                 'If you incorporate with Karman and use our <a href="/services/accounting">accounting service</a>, InvoiceNow setup is included. We pick the right accounting system (Xero is our default), configure your Peppol ID, register with IMDA, and connect transmission to IRAS - usually before your first GST filing is due.',
                 "If you've already incorporated and want help migrating, our accounting team can audit your current setup and migrate you onto an InvoiceNow-ready stack. The earlier you do this, the smoother subsequent GST filing cycles will be.",
             ]),
        ],
        "faqs": [
            ("Do I need InvoiceNow if my business is not GST-registered?",
             "No - InvoiceNow GST reporting only applies to GST-registered businesses. However, you can still use the Peppol network to send invoices to customers who are on it. Many Karman clients adopt InvoiceNow before GST registration to streamline B2B invoicing."),
            ("What happens if I don't comply by April 2026?",
             "Failure to comply with the InvoiceNow GST requirement is treated as a GST registration condition breach. IRAS can refuse to process your GST registration or, for already-registered companies covered by future mandates, impose penalties consistent with other GST non-compliance (S$200-S$1,000 administrative penalties, plus continued non-compliance can attract compounded penalties)."),
            ("Does InvoiceNow replace my GST F5 return?",
             "No. You still file the GST F5 return quarterly (or monthly, depending on your filing frequency). InvoiceNow transmits the underlying transaction data to IRAS, which makes the F5 reconciliation simpler and refund verification faster, but the F5 return is still submitted via the myTax Portal."),
            ("Can I use InvoiceNow with Xero or Quickbooks?",
             "Yes. Both Xero and Quickbooks Online support InvoiceNow / Peppol e-invoicing in Singapore. Xero has native support; Quickbooks works through certified access-point providers. Karman uses Xero by default for accounting clients - InvoiceNow is configured during onboarding."),
            ("Is InvoiceNow only for Singapore-to-Singapore invoices?",
             "No. The Peppol network is international. You can send invoices to customers in Australia, New Zealand, EU member states, Japan, Malaysia, and any other Peppol-enabled jurisdiction. Domestic Singapore invoices flow into IRAS for GST reporting; international invoices flow to the recipient but don't typically trigger GST reporting (since exports are zero-rated)."),
        ],
        "sources": [
            ("https://www.iras.gov.sg/taxes/goods-services-tax-(gst)/getting-it-right/general-rules-on-invoicenow-for-gst", "IRAS - InvoiceNow for GST"),
            ("https://www.imda.gov.sg/how-we-can-help/nationwide-e-invoicing-framework", "IMDA - Nationwide E-Invoicing Framework"),
            ("https://www.iras.gov.sg/taxes/goods-services-tax-(gst)", "IRAS - Goods and Services Tax"),
        ],
        "related": [
            ("when-to-register-gst-singapore", "GST", "gst", "When Does Your Singapore Company Need to Register for GST?", "Compulsory threshold, voluntary registration, and the cost-benefit analysis.", "7 min read"),
            ("singapore-company-annual-compliance-checklist", "Compliance", "compliance", "Singapore Company Annual Compliance Checklist", "Month-by-month deadlines for ACRA, IRAS, CPF, and GST filings.", "8 min read"),
            ("singapore-corporate-tax-guide-small-business", "Tax", "tax", "Singapore Corporate Tax Guide for Small Businesses (2026)", "17% rate, StartUp Tax Exemption, ECI filing, and worked examples.", "9 min read"),
        ],
    },

    # ------------------------------------------------------------------
    # 2. Budget 2026 corporate tax
    # ------------------------------------------------------------------
    {
        "slug": "singapore-budget-2026-corporate-tax",
        "title": "Singapore Budget 2026: Corporate Tax Rebate, AI Deductions Explained",
        "description": "Singapore Budget 2026 gives founders a 40% Corporate Income Tax rebate (up to S$30K) and a 400% AI Enterprise Innovation deduction. Here's how to use both.",
        "keyword": "singapore budget 2026 corporate tax",
        "tag": "Tax",
        "tag_class": "tax",
        "breadcrumb_short": "Budget 2026 Tax",
        "read_min": 8,
        "lede": "Singapore's Budget 2026 was announced in February 2026 and brings two changes that matter to founders: a <strong>40% Corporate Income Tax (CIT) rebate</strong> for YA 2026 and a meaningfully expanded <strong>Enterprise Innovation Scheme (EIS)</strong> with up to 400% deduction on qualifying AI and R&D spend. If you have a Singapore Pte Ltd, both apply automatically once you file - but you need to know what counts and how to maximise them.",
        "intro_p2": "This piece explains what the rebate is, what the AI deduction covers, the caps and exclusions, and how to think about timing your spend if you can.",
        "sections": [
            ("The 40% CIT rebate (YA 2026 only)",
             [
                 "Every active company in Singapore receives a 40% rebate on its corporate income tax payable for Year of Assessment 2026, capped at S$30,000.",
                 "<strong>How it works:</strong> After you compute your CIT (17% headline less Startup Tax Exemption or Partial Tax Exemption), the rebate is applied. If your CIT payable is S$10,000, you pay S$6,000. If it's S$100,000, the rebate is capped at S$30,000.",
                 '<div class="callout callout--teal"><div class="callout__title">Worked example</div><p>Profit: S$300,000. Tax (post-Startup Tax Exemption): S$24,250. CIT rebate at 40%: S$9,700. Final tax: S$14,550.</p><p>Profit: S$1,000,000 (mature company, no SUTE). Tax: S$170,000. CIT rebate: capped at S$30,000. Final tax: S$140,000.</p></div>',
                 "<strong>Cash payout component:</strong> Active companies that employed at least one local employee in 2025 (with CPF contributions) get a minimum cash payout of S$2,000, even if they have no CIT payable. This is automatically credited to your bank account on file with IRAS.",
                 "<strong>Who qualifies:</strong> Any Singapore tax-resident company with chargeable income for YA 2026. There's no application - the rebate is computed automatically when you file your Form C-S or Form C.",
             ]),
            ("The 400% AI / R&D deduction (Enterprise Innovation Scheme)",
             [
                 "The Enterprise Innovation Scheme (EIS) was introduced in Budget 2023 and meaningfully expanded in Budget 2024 and 2026. For YA 2026 specifically, qualifying AI spend gets a <strong>400% tax deduction on the first S$50,000</strong> (versus 100% as a normal deduction).",
                 "Translated: every dollar of qualifying AI spend gives you S$4 of tax deduction, up to S$50,000 of spend per year. That's a 17% × S$200,000 = <strong>S$34,000 reduction</strong> in tax payable, against S$50,000 of cash spend.",
                 "<strong>What qualifies as AI spend (per IRAS guidance):</strong>",
                 "<ul><li>Subscription fees for AI development platforms (e.g., enterprise OpenAI, Anthropic API, Google Vertex AI when used for development not just inference)</li><li>Cloud compute for AI model training and fine-tuning</li><li>AI-related software development (including the salary cost of engineers building AI products)</li><li>Acquisition of AI-related IP or AI-trained models</li><li>Specialised AI hardware (GPUs, TPUs)</li></ul>",
                 "<strong>What doesn't qualify:</strong> General productivity software (e.g., generic ChatGPT subscriptions for staff use), AI-as-a-feature in non-AI software, and inference-only API calls used in production (those are normal operating expenses, not innovation expenditure).",
             ]),
            ("Other EIS components worth knowing",
             [
                 "EIS covers more than AI. Other qualifying activities, each with their own caps and rates:",
                 "<ul><li><strong>R&D expenditure:</strong> 400% deduction on first S$400,000 of qualifying R&D activities (very generous)</li><li><strong>IP registration fees:</strong> 400% deduction on first S$50,000 (patents, trademarks, designs, plant varieties)</li><li><strong>IP acquisition and licensing:</strong> 400% deduction on first S$400,000 (combined with IP registration cap)</li><li><strong>Employee training:</strong> 400% deduction on first S$50,000 (must be SkillsFuture-approved courses)</li><li><strong>Innovation projects with partner institutions:</strong> 400% deduction on first S$50,000 (collaborations with polytechnics, ITE, A*STAR)</li></ul>",
                 "<strong>Cash payout option:</strong> Companies (especially those with little or no taxable profit) can opt to convert up to S$100,000 of qualifying EIS expenditure into a non-taxable cash payout at 20%. Translated: S$100,000 of qualifying spend → S$20,000 cash from IRAS, instead of a tax deduction. Useful for early-stage companies that aren't yet profitable.",
             ]),
            ("How to claim",
             [
                 "Both the 40% CIT rebate and the EIS are claimed in your annual corporate tax return (Form C-S or Form C):",
                 "<ol><li><strong>CIT rebate:</strong> Computed automatically when you file. No separate claim form.</li><li><strong>EIS deduction:</strong> Disclosed in the relevant section of Form C-S/C. You'll need supporting documentation: invoices, project descriptions, evidence of qualifying activity. IRAS may request these during desk audit.</li><li><strong>EIS cash payout:</strong> Separate election in your tax return. Cash is paid out within ~3 months of filing.</li></ol>",
                 "<strong>Documentation matters.</strong> EIS claims are audit-prone. Keep invoices, contracts, time-tracking for engineering staff working on R&D, and project descriptions documented as you go - not retroactively. IRAS publishes a detailed e-Tax Guide on the EIS that lists exactly what evidence they expect.",
             ]),
            ("Timing your spend (if you have flexibility)",
             [
                 "If you're a profitable company and have planned AI/R&D/training/IP spend that could fall in either YA 2026 or YA 2027, the answer depends on the rate that applies to your YA. The 400% deduction has been confirmed for YA 2025-YA 2028 across most categories, so timing typically doesn't change much.",
                 "What does matter for timing: the <strong>40% CIT rebate is YA 2026 only</strong>. If you can accelerate revenue or defer deductions into YA 2026, you trade one dollar of tax saved at 17% later for one dollar saved at 17% × (1 - 40%) = 10.2% now. That's a 6.8% timing benefit on tax payable.",
                 "Don't manufacture transactions for tax timing - but if you're already deciding whether to invoice in December 2025 or January 2026 (where Jan falls into YA 2026), the rebate is a genuine reason to choose Jan.",
             ]),
            ("Who benefits most",
             [
                 "<strong>Profitable mature SMEs</strong>: The 40% CIT rebate hits the cap at S$75,000 of CIT payable, which is roughly S$440,000 of profit (post-PTE). Above that, marginal benefit drops. This makes it most valuable for companies in the S$200K-S$500K profit band.",
                 "<strong>AI / SaaS startups</strong>: The 400% AI deduction is genuinely material. A pre-revenue startup spending S$50,000 on AI development gets either a S$200,000 tax deduction (carried forward as losses) or a S$10,000 cash payout (under the cash conversion option). For early-stage AI companies on the Karman <a href=\"/for/ai-startups\">/for/ai-startups</a> path, this is real money.",
                 "<strong>Founders with IP investment</strong>: Patent registration, IP acquisition, and licensing all qualify at 400% on the first tranche of spend. If you've been deferring trademark or patent filings, YA 2026 is the year.",
             ]),
            ("What changed vs Budget 2025",
             [
                 "Three substantive changes to be aware of:",
                 "<ol><li>The <strong>40% CIT rebate is new</strong> - YA 2025 had no rebate. Budget 2026 is one-off, not a permanent change.</li><li>The <strong>AI-specific 400% category was carved out</strong> from general R&D in Budget 2026, with its own S$50,000 cap. Previously, AI work was claimed under general R&D. The carve-out means founders can't double-count the same spend - if it's AI, it sits in the AI bucket; if it's broader R&D, it sits in the R&D bucket.</li><li><strong>Cash payout flexibility increased</strong> - the conversion ratio (20%) is unchanged but the qualifying activities list was broadened to include more software and AI activities.</li></ol>",
             ]),
        ],
        "faqs": [
            ("Do I need to apply for the 40% CIT rebate?",
             "No. The rebate is automatically computed when you file Form C-S or Form C for YA 2026. There's no separate application. The cash payout (minimum S$2,000) is also automatic for active companies that employed at least one local employee in 2025."),
            ("Can a loss-making company benefit from the EIS?",
             "Yes - through the cash payout option. Loss-making companies can convert up to S$100,000 of qualifying EIS expenditure into a non-taxable cash payout at 20% (so S$100K spend → S$20K cash from IRAS). The alternative is to carry forward the tax deduction as losses, which has value only when the company becomes profitable later."),
            ("What counts as 'AI spend' for the 400% deduction?",
             "IRAS guidance includes: AI development platform subscriptions, cloud compute for training and fine-tuning, salary costs of engineers building AI products, acquisition of AI IP or trained models, and AI-specific hardware. It does NOT include generic ChatGPT subscriptions for staff productivity, AI-as-a-feature in non-AI software, or inference API calls used in routine production."),
            ("Does the CIT rebate stack with the StartUp Tax Exemption?",
             "Yes. The rebate is applied AFTER your tax exemption schemes are computed. So a Year-1 startup with S$200,000 profit pays roughly S$12,750 under SUTE, then gets a 40% rebate on that, paying S$7,650 - about a 3.8% effective rate."),
            ("When are EIS claims audited?",
             "IRAS conducts desk audits on a sample basis, typically 12-24 months after filing. They request invoices, project descriptions, and evidence of qualifying activity. Maintain documentation contemporaneously - retroactive justification rarely satisfies the auditor. Karman's accounting service handles EIS documentation as part of standard bookkeeping for AI/SaaS clients."),
        ],
        "sources": [
            ("https://www.mof.gov.sg/singaporebudget", "Singapore Ministry of Finance - Budget 2026"),
            ("https://www.iras.gov.sg/schemes/disbursement-schemes/corporate-income-tax-rebate", "IRAS - Corporate Income Tax Rebate"),
            ("https://www.iras.gov.sg/schemes/disbursement-schemes/enterprise-innovation-scheme-(eis)", "IRAS - Enterprise Innovation Scheme"),
        ],
        "related": [
            ("singapore-corporate-tax-guide-small-business", "Tax", "tax", "Singapore Corporate Tax Guide for Small Businesses (2026)", "17% rate, StartUp Tax Exemption, ECI filing, and worked examples.", "9 min read"),
            ("ai-startups-incorporating-singapore-2026", "Industry", "guide", "AI Startups Incorporating in Singapore (2026)", "Why AI founders pick Singapore Pte Ltd, with structure and tax angles.", "10 min read"),
            ("oecd-pillar-two-singapore-holding-company", "Tax", "tax", "OECD Pillar Two and Your Singapore Holding Company", "What the 15% global minimum tax means for Singapore-structured groups.", "9 min read"),
        ],
    },

    # ------------------------------------------------------------------
    # 3. COMPASS 2026 EP renewal
    # ------------------------------------------------------------------
    {
        "slug": "compass-framework-2026-ep-renewal",
        "title": "COMPASS 2026 Update: New EP Salary & Renewal Rules for Founders",
        "description": "From 1 July 2026, MOM applies COMPASS to Employment Pass renewals - not just new applications. Salary thresholds rose in January 2026. What founders must know.",
        "keyword": "compass framework 2026 singapore",
        "tag": "Visas",
        "tag_class": "guide",
        "breadcrumb_short": "COMPASS 2026 EP",
        "read_min": 9,
        "lede": "<strong>From 1 July 2026, the Complementarity Assessment Framework (COMPASS) applies to Employment Pass renewals</strong> - not just new applications. Combined with the January 2026 salary increase, this is the biggest tightening of the EP regime since COMPASS launched. If you're a founder on EP, hiring on EP, or planning to renew, this is the brief.",
        "intro_p2": "COMPASS is MOM's points-based scoring system for EP applications. It scores candidates and their employer across four core attributes (salary, qualifications, diversity, support for locals) plus two bonus attributes (skills shortage, strategic priorities). Until July 2026, COMPASS only applied to new applications and very high-volume renewals. From July it applies to all EPs at renewal.",
        "sections": [
            ("What changed in 2026 (at a glance)",
             [
                 "<strong>1 January 2026 - Salary thresholds raised:</strong>",
                 "<ul><li>EP minimum qualifying salary (general): S$5,600/month (up from S$5,000)</li><li>EP minimum qualifying salary (financial services): S$6,200/month (up from S$5,500)</li><li>S Pass minimum qualifying salary: S$3,300/month (up from S$3,150)</li><li>Older candidates (mid-40s+) face progressively higher minimums</li></ul>",
                 "<strong>1 July 2026 - COMPASS applies to renewals:</strong>",
                 "<ul><li>All EP renewal applications must score at least 40 points across the COMPASS framework</li><li>Renewals failing COMPASS will not be granted, regardless of how long the EP has been held</li><li>Some narrowly-defined exemption categories continue (e.g., overseas networks talent, government-endorsed strategic hires)</li></ul>",
                 'See our <a href="/glossary/ep">Employment Pass glossary entry</a> for the full eligibility framework.',
             ]),
            ("How COMPASS scoring actually works",
             [
                 "Every EP application (new or renewal from July 2026) must score at least 40 points across these attributes:",
                 '<div class="table-wrap"><table><thead><tr><th>Attribute</th><th>0 points</th><th>10 points</th><th>20 points</th></tr></thead><tbody><tr><td>C1 Salary</td><td>Below 50th percentile of local PMETs in same sector</td><td>50th-65th percentile</td><td>65th percentile and above</td></tr><tr><td>C2 Qualifications</td><td>No degree</td><td>Degree from acceptable institution</td><td>Top-tier institution (e.g., QS/THE top 100)</td></tr><tr><td>C3 Diversity</td><td>Same nationality is &gt;25% of company PMET workforce</td><td>5-25%</td><td>Below 5%</td></tr><tr><td>C4 Support for locals</td><td>Below industry average for local PMET hiring</td><td>At industry average</td><td>Above industry average</td></tr></tbody></table></div>',
                 "<strong>Plus bonus attributes (additional 10-20 points):</strong>",
                 "<ul><li>C5 Skills bonus: candidate's role is on the Shortage Occupation List (typically tech, healthcare, advanced manufacturing)</li><li>C6 Strategic Economic Priorities: company's investment commitments align with national priorities</li></ul>",
                 "Pass mark: 40 points. Most successful applications score in the 40-80 point range.",
             ]),
            ("Why renewals are now the binding constraint",
             [
                 "Until July 2026, an EP holder could renew almost automatically at the prevailing salary. From July 2026, the renewal goes through the same COMPASS scoring as a new application.",
                 "<strong>What this means in practice:</strong> A founder or employee who was hired in 2022 at S$5,500 and never received a meaningful raise might now be below the C1 salary band for 2026. If their company is C3-weak (e.g., a 5-person team where 4 are the same nationality) and C4-weak (no local hires), the renewal could fail.",
                 "<strong>Founders especially:</strong> If you're the sole director and EP holder of a small company, you have limited C4 (Support for locals) score - because there are no local employees to support. This can be offset by C1 (high salary), C2 (top-tier qualifications), or by hiring local PMETs.",
             ]),
            ("Pre-renewal action plan (12 months out)",
             [
                 "If your EP renewal is coming up in mid-2026 or 2027, work backwards 12 months and audit each COMPASS attribute:",
                 "<strong>C1 - Salary</strong>: Compare your current salary to the 50th and 65th percentile for PMETs in your sector. MOM publishes these benchmarks. If you're below the 50th, you score 0 on C1, which means you need to score 40+ on the other attributes alone. The simplest fix: raise your salary above the 65th percentile if your company can afford it. Self-employed founders often pay themselves more in salary and less in dividends specifically to satisfy COMPASS.",
                 "<strong>C2 - Qualifications</strong>: Static (you can't change your degree retroactively). If your degree is from a non-recognised institution, you score 0 on C2. Compensating: lift other attributes.",
                 "<strong>C3 - Diversity</strong>: Look at your PMET headcount by nationality. If &gt;25% are the same nationality as you, you score 0. Hiring local PMETs reduces this percentage. So does hiring PMETs of different nationalities.",
                 "<strong>C4 - Support for locals</strong>: Hire local PMETs. The benchmark is industry-relative, so you don't need a 50/50 split - you need to be at or above the average for your industry. For tech companies, hiring 1-2 local engineers can shift you from below to above average if you're a small team.",
                 "<strong>C5 / C6 (bonus)</strong>: Check if your role is on the Shortage Occupation List. Tech roles (software engineering, AI/ML, cybersecurity) often qualify. Investment commitments via EDB endorsement can give C6 bonus points but require a real engagement.",
             ]),
            ("What happens if your renewal fails",
             [
                 "If MOM rejects your renewal, you have a 1-month appeal window. The appeal must be substantive - new evidence, new salary commitment, new local hires.",
                 "If the appeal fails, your EP expires on its current expiry date and you must leave Singapore (or transition to another pass). For founders, this is severely disruptive: bank accounts, tenancy, schooling, and company directorship are all tied to your EP.",
                 "<strong>Backup pathways for founders:</strong>",
                 "<ul><li>Tech.Pass - sponsor-free pass for senior tech professionals; criteria include US$20K+ monthly salary OR 5+ years at a leading tech company OR a product with 100K+ users</li><li>ONE Pass - top-tier pass requiring S$30,000 monthly salary; 5-year duration</li><li>Permanent Residence - if you've been on EP for 4+ years with strong COMPASS profile, PR application is the durable solution</li></ul>",
             ]),
            ("Founder-specific edge cases",
             [
                 "<strong>Sole director, sole employee, all-foreign team</strong>: Highest renewal risk. C4 is structurally weak. Mitigation: hire local PMETs (even 1-2 makes a meaningful difference), or transition the team toward a local-majority PMET base over 12-18 months.",
                 "<strong>Pre-revenue startup paying founder below market</strong>: Many founders pay themselves the EP minimum to conserve cash. This scores 0 on C1 from January 2026 (since S$5,600 is now likely below 50th percentile in tech). Mitigation: time the salary increase to coincide with renewal cycle, or supplement with bonuses that count toward gross monthly income.",
                 "<strong>Family office / wealth structure with offshore-resident founder</strong>: Some structures use a Singapore Pte Ltd with the founder as director but not employee. Renewal isn't relevant in those cases (no EP held), but if you do hold an EP, ensure your role and salary stand up to MOM scrutiny - a nominal director role with no operational responsibility may be flagged.",
             ]),
            ("How Karman supports EP renewals",
             [
                 "Karman's incorporation and corporate secretary services include EP application and renewal support. We run a COMPASS pre-check 6 months before renewal, identify which attributes are at risk, and recommend specific changes (salary timing, hire timing, role documentation) to maximise renewal probability.",
                 'For founders building team around them, see our <a href="/for/ai-startups">/for/ai-startups</a>, <a href="/for/saas">/for/saas</a>, and <a href="/for/fintech">/for/fintech</a> industry pages for sector-specific EP planning.',
             ]),
        ],
        "faqs": [
            ("When does COMPASS apply to EP renewals?",
             "From 1 July 2026, COMPASS applies to all EP renewal applications. Before that date, renewals are typically processed under the prevailing salary criteria. Applications submitted before 1 July 2026 are assessed under the pre-July framework even if a decision is issued after that date."),
            ("What's the minimum EP salary in Singapore in 2026?",
             "From 1 January 2026: S$5,600/month for general roles, S$6,200/month for financial services. These minimums increase progressively for older candidates (mid-40s+). The salary must also pass C1 in COMPASS - which means being at or above the 50th percentile for PMETs in your sector. The minimum and the C1 benchmark can differ; both must be satisfied."),
            ("Can my EP be rejected at renewal even if my salary increased?",
             "Yes. Salary alone is one of four core attributes plus two bonus attributes in COMPASS. A high salary can score 20 points on C1 but still fail to reach the 40-point pass mark if the company scores 0 on C3 (diversity) and C4 (support for locals). MOM looks at the whole picture."),
            ("Does hiring a Singaporean local help my COMPASS score?",
             "Yes - it improves both C3 (Diversity, by reducing the same-nationality concentration in your PMET workforce) and C4 (Support for locals, by raising your local PMET ratio). For small companies, a single local PMET hire can shift you from 0 to 10 or 20 points on these attributes."),
            ("What if my EP renewal fails?",
             "You have a 1-month appeal window. If the appeal fails, your EP expires and you must leave Singapore by the expiry date or transition to another pass. Realistic alternatives: Tech.Pass (for senior tech professionals), ONE Pass (S$30K monthly salary requirement), or Permanent Residence application (if you have 4+ years on EP and a strong profile)."),
        ],
        "sources": [
            ("https://www.mom.gov.sg/passes-and-permits/employment-pass/eligibility", "MOM - Employment Pass Eligibility"),
            ("https://www.mom.gov.sg/passes-and-permits/employment-pass/eligibility/complementarity-assessment-framework", "MOM - COMPASS Framework"),
            ("https://www.mom.gov.sg/passes-and-permits/employment-pass/eligibility/qualifying-salaries", "MOM - EP Qualifying Salaries"),
        ],
        "related": [
            ("singapore-employment-pass-company-director", "Visas", "guide", "Singapore Employment Pass for Company Directors", "How to qualify for an EP as a founder of a Singapore Pte Ltd.", "8 min read"),
            ("nominee-director-singapore-complete-guide", "Compliance", "compliance", "Nominee Director in Singapore: Complete Guide", "When to use one, what they do, and what they don't do.", "10 min read"),
            ("singapore-bank-account-foreign-company", "Banking", "guide", "Opening a Bank Account for a Foreign-Owned Singapore Company", "DBS, OCBC, UOB, Aspire, Wise - what works for foreign founders.", "9 min read"),
        ],
    },

    # ------------------------------------------------------------------
    # 4. Pay yourself salary vs dividend
    # ------------------------------------------------------------------
    {
        "slug": "pay-yourself-singapore-pte-ltd",
        "title": "Singapore Pte Ltd: How to Pay Yourself - Salary vs Dividend (2026)",
        "description": "Salary, dividends, or both? A practical guide for Singapore Pte Ltd founders - tax, CPF, EP, paperwork, and the right mix at different revenue stages.",
        "keyword": "pay yourself singapore pte ltd",
        "tag": "Tax",
        "tag_class": "tax",
        "breadcrumb_short": "Salary vs Dividend",
        "read_min": 10,
        "lede": "Once your Singapore Pte Ltd is profitable, the question every founder asks is: <strong>how do I actually pay myself?</strong> The two main options - salary and dividends - have different tax treatment, different CPF implications, different rules, and different paperwork. The right mix depends on whether you're on EP, your residency status, your company's profit level, and your personal needs.",
        "intro_p2": "This is the most frequently asked operational question after incorporation. Here's the practical playbook: how each works, when each is taxed, and the optimal mix at different stages.",
        "sections": [
            ("The two main payment routes",
             [
                 "Your Singapore Pte Ltd can pay you in two distinct ways:",
                 "<ol><li><strong>Salary (employment income)</strong> - you appoint yourself as an employee/director, agree a monthly wage, and the company processes payroll like any other employee. Salary is tax-deductible to the company (reducing CIT) and is personally taxed at progressive rates.</li><li><strong>Dividends (shareholder distribution)</strong> - the company declares dividends from after-tax retained earnings and pays them to you as a shareholder. Dividends are NOT tax-deductible to the company but are tax-free in your hands (one-tier system).</li></ol>",
                 "<strong>Singapore's one-tier corporate tax system is the key concept:</strong> the company pays 17% CIT on profits, then dividends from those after-tax profits are not taxed again. This is genuinely founder-friendly - many other jurisdictions tax dividends a second time at the personal level.",
             ]),
            ("Salary: how it works in detail",
             [
                 "<strong>Tax treatment</strong>: Salary is tax-deductible to the company. So S$10,000 of salary reduces the company's chargeable income by S$10,000 and the CIT bill by S$1,700 (at the 17% headline rate). On your side, the salary is taxed at Singapore personal income tax rates - which range from 0% (first S$20K) to 24% (top bracket).",
                 "<strong>CPF</strong>: If you're a Singapore Citizen or PR, both you and the company contribute CPF (Central Provident Fund) on the salary. Combined rates are around 37% for under-55s, capped at the Ordinary Wage ceiling (S$7,400/month from 2026, rising to S$8,000 in 2027). For foreign employees and EP holders, no CPF.",
                 "<strong>EP holders</strong>: Salary is the main route to satisfy EP qualifying salary requirements. You must be paid the EP minimum (S$5,600/month general, S$6,200 financial services from January 2026) and your salary feeds C1 in COMPASS scoring. <a href=\"/blog/compass-framework-2026-ep-renewal\">Read our COMPASS 2026 guide</a> for renewal-relevant detail.",
                 "<strong>Paperwork</strong>: Monthly payroll filing (or via accounting software), annual IR8A return to IRAS by 1 March, and CPF submission monthly (where applicable).",
             ]),
            ("Dividends: how it works in detail",
             [
                 "<strong>Tax treatment</strong>: Dividends come from after-tax retained earnings. The company has already paid 17% CIT on the profits used to fund the dividend. There is no further personal tax on the dividend in Singapore. The recipient receives the gross amount.",
                 "<strong>CPF</strong>: None. Dividends are not employment income, so no CPF contribution applies - even for Citizens and PRs.",
                 "<strong>EP holders</strong>: Dividends do NOT count toward EP qualifying salary. Paying yourself only via dividends, with no salary, will fail EP requirements. EP holders must have a real salary at the qualifying threshold.",
                 "<strong>Paperwork</strong>: Board resolution authorising the dividend, dividend voucher to the shareholder, entry in the company's financial accounts. No filing with IRAS for the dividend itself (since it's not taxable).",
                 '<a href="/templates/board-resolution">Karman provides a free Board Resolution template</a> covering dividend declarations.',
             ]),
            ("Worked example: Year-1 startup with S$200,000 profit",
             [
                 "Suppose you're a Singapore Citizen founder. Your Pte Ltd has S$200,000 of profit before founder compensation in its first year (so SUTE applies).",
                 '<div class="callout callout--teal"><div class="callout__title">Scenario A: All salary (S$200K salary, S$0 profit)</div><p>Company pays no CIT (profit is zero after salary). Personal income S$200K → roughly S$23,000 personal tax (effective ~11.5%) plus CPF ~S$31,000 (combined employer + employee). <strong>Total taxes/CPF: ~S$54,000.</strong></p><p>You receive: S$200K salary minus your CPF (~S$15,000) minus personal tax (~S$23,000) = ~S$162,000 net cash, of which ~S$15,000 goes into your CPF account.</p></div>',
                 '<div class="callout callout--amber"><div class="callout__title">Scenario B: Salary S$72K + dividend S$120K</div><p>Salary chosen at S$6,000/month (above EP minimum, low personal tax bracket). Profit before tax becomes S$200K - S$72K = S$128K. CIT under SUTE: S$128K → first S$100K at 4.25% = S$4,250; next S$28K at 8.5% = S$2,380; total CIT ~S$6,630. After-tax retained earnings ~S$121K. Declare S$120K dividend.</p><p>Personal: salary tax on S$72K ~S$2,000 (low bracket); dividends tax-free; CPF on S$72K ~S$11,000 combined. <strong>Total taxes/CPF: ~S$20,000.</strong></p><p>You receive: S$72K salary minus CPF (~S$5,500) minus tax (~S$2,000) + S$120K dividend = ~S$184,500 net cash, of which ~S$5,500 goes into CPF.</p></div>',
                 "Net cash difference: ~S$22,500 in favour of the salary+dividend mix. The reason: lower-bracket personal income tax + the SUTE shielding most of the dividend-funding profit.",
                 "<strong>Caveats</strong>: This example assumes you're a Singapore Citizen. For an EP holder, Scenario A or B both work as long as salary stays at/above EP minimums. For non-residents, dividend tax treatment is the same (no Singapore WHT on dividends), but personal salary tax may be different.",
             ]),
            ("The right mix at different stages",
             [
                 "<strong>Pre-profit / pre-revenue</strong>: You probably can't pay yourself meaningfully. If you're an EP holder, you must still meet the EP salary minimum - so salary at S$5,600/month is the floor. Founders sometimes lend the company money personally to fund this through dry months. Dividends are not relevant until the company is profitable.",
                 "<strong>Year 1-3 (SUTE active)</strong>: Mix matters. Personal income tax is progressive, so high salary pushes you into 15%+ brackets unnecessarily. Meanwhile CIT under SUTE is just 4.25% on the first S$100K of profit. <strong>The general rule</strong>: pay yourself a salary that satisfies EP requirements (or covers your living expenses if you're a citizen/PR) and take dividends from any remaining profit. For most founders this means S$60K-S$120K salary and the rest as dividend.",
                 "<strong>Year 4+ (Partial Tax Exemption)</strong>: SUTE is gone. CIT is now closer to 8-9% effective up to S$200K profit, then 17% above. Salary becomes more attractive at the margin (since each dollar of salary reduces CIT at 17%). Founders often shift slightly more weight to salary.",
                 "<strong>Mature profitable company (post-S$1M profit)</strong>: At this scale, the dividend route saves real money. Personal tax brackets max out at 24% above S$320K of personal income. Dividend at 0% personal tax beats salary at 24% personal tax + 0% CPF (foreigners) or 24% + 37% CPF (citizens/PRs). Most mature founders settle on a salary that covers personal cash needs + EP / CPF requirements, with the bulk of compensation as dividend.",
             ]),
            ("Common mistakes founders make",
             [
                 "<strong>Mistake 1: Paying yourself only dividend while on EP.</strong> EP requires a qualifying salary. No salary = EP renewal failure. Always pay yourself at least the EP minimum.",
                 "<strong>Mistake 2: Declaring dividends without proper paperwork.</strong> Dividends require a board resolution and proper accounting entries. Without these, IRAS or ACRA may treat the payment as a director's loan or unauthorised distribution. Use Karman's free <a href=\"/templates/board-resolution\">Board Resolution template</a>.",
                 "<strong>Mistake 3: Paying dividends before paying CIT.</strong> Dividends come from after-tax retained earnings. If the company hasn't paid its CIT yet for the relevant YA, technically it doesn't have distributable retained earnings. Most founders and accountants accrue the expected tax liability before declaring dividends.",
                 "<strong>Mistake 4: Forgetting CPF for citizen/PR directors.</strong> Both you and the company owe CPF on salary if you're a Singapore Citizen or PR. Missing this for 12 months gets expensive fast - back contributions plus penalties.",
                 "<strong>Mistake 5: Setting salary below market 'because it's just yourself'.</strong> If your Form C-S is audited, IRAS may impute a market salary and disallow dividend characterisation. More commonly: low salary kills your COMPASS C1 score at EP renewal.",
             ]),
            ("How Karman handles this for clients",
             [
                 "Karman's accounting service includes monthly payroll, IR8A filing, dividend documentation, and an annual review of your salary-dividend mix as your company moves through its tax stages.",
                 "Tools that help you plan: our <a href=\"/tools/cost-calculator\">cost calculator</a> includes founder compensation modelling, and our <a href=\"/glossary/corporate-tax\">corporate tax glossary entry</a> explains the underlying rates.",
             ]),
        ],
        "faqs": [
            ("Is dividend income tax-free in Singapore?",
             "Yes. Singapore uses a one-tier corporate tax system: the company pays 17% CIT on profits, and dividends paid from those after-tax profits are not taxed again - either in the company's hands or the shareholder's hands. This applies to both individual and corporate shareholders, resident and non-resident."),
            ("Do I have to pay myself a salary as a Singapore Pte Ltd director?",
             "Not if you're a Singapore Citizen, PR, or non-resident with no EP. You can be an unpaid director and only take dividends. However, if you hold an Employment Pass, you must be a paid employee at the EP qualifying salary minimum - the EP requires real employment, not just a directorship."),
            ("Can I retroactively re-classify salary as dividend?",
             "No. Once you've paid yourself a salary and the company has filed payroll/IR8A reflecting it, that classification is final for that year. To shift the mix, change the structure for the upcoming YA: reduce salary going forward, accumulate retained earnings, and declare dividends from them. Don't try to unwind prior payments - it triggers IRAS scrutiny."),
            ("Do I owe CPF on dividends?",
             "No. CPF only applies to salary and bonuses (employment income). Dividends are shareholder distributions, not employment income, and carry no CPF obligation - even for Singapore Citizens and PRs."),
            ("What's the optimal salary-dividend mix?",
             "Depends on your residency, EP status, and the company's stage. General rule for Singapore Citizens/PRs in a profitable startup: S$60K-S$120K salary plus dividends from remaining profit during SUTE years (Year 1-3). For EP holders: salary at or above EP qualifying minimum (S$5,600-S$6,200/month from 2026), and dividends on top. Karman's accounting team runs this analysis annually for clients."),
        ],
        "sources": [
            ("https://www.iras.gov.sg/taxes/individual-income-tax/employees/working-out-your-taxes/working-out-your-pay/dividend-income", "IRAS - Dividend Income"),
            ("https://www.iras.gov.sg/taxes/individual-income-tax/basics-of-individual-income-tax/tax-residency-and-tax-rates/tax-rates", "IRAS - Personal Income Tax Rates"),
            ("https://www.cpf.gov.sg/employer/employer-obligations/contribution-rates", "CPF - Employer Contribution Rates"),
            ("https://www.iras.gov.sg/schemes/disbursement-schemes/start-up-tax-exemption-scheme", "IRAS - Start-Up Tax Exemption"),
        ],
        "related": [
            ("singapore-corporate-tax-guide-small-business", "Tax", "tax", "Singapore Corporate Tax Guide for Small Businesses (2026)", "17% rate, StartUp Tax Exemption, ECI filing, and worked examples.", "9 min read"),
            ("compass-framework-2026-ep-renewal", "Visas", "guide", "COMPASS 2026 Update: New EP Salary & Renewal Rules", "Salary thresholds and renewal rules every founder must know.", "9 min read"),
            ("singapore-company-annual-compliance-checklist", "Compliance", "compliance", "Singapore Company Annual Compliance Checklist", "Month-by-month deadlines for ACRA, IRAS, CPF, and GST filings.", "8 min read"),
        ],
    },

    # ------------------------------------------------------------------
    # 5. Vietnamese founders
    # ------------------------------------------------------------------
    {
        "slug": "singapore-company-incorporation-vietnamese-founders",
        "title": "Singapore Company Incorporation for Vietnamese Founders (2026)",
        "description": "Vietnamese founders incorporating in Singapore: Pte Ltd vs Vietnam, banking, FX restrictions, Vietnam-Singapore DTAA, EP options, and remittance rules.",
        "keyword": "singapore company vietnamese founder",
        "tag": "Foreign Founders",
        "tag_class": "guide",
        "breadcrumb_short": "Vietnamese Founders",
        "read_min": 10,
        "lede": "Vietnamese founders are increasingly choosing Singapore for their holding company, regional headquarters, or international operating entity. The reasons are practical: better access to global investors, banking that works across currencies, a Vietnam-Singapore double tax agreement, and a regulatory environment that's easier to navigate than Vietnam's foreign investment regime. Here's the full playbook for Vietnamese founders.",
        "intro_p2": "This guide covers when Singapore makes sense, what to incorporate, how to handle the State Bank of Vietnam (SBV) FX restrictions on outward investment, banking pathways, EP options for relocating, and the tax interaction between Vietnam and Singapore.",
        "sections": [
            ("Why Vietnamese founders choose Singapore",
             [
                 "Four reasons drive most Vietnamese founders to incorporate in Singapore - usually as a holding company over their Vietnamese operating entity, or as a standalone international company:",
                 "<ul><li><strong>Investor accessibility</strong>. International VCs (US, EU, regional Asia funds) prefer to invest into a Singapore Pte Ltd over a Vietnamese Limited Liability Company. Cap table mechanics, share rights, and exit pathways are well-understood by Singapore lawyers and arbitrators.</li><li><strong>Banking and global payments</strong>. Singapore banks (DBS, OCBC, UOB) plus Aspire and Wise Business handle multi-currency easily. Vietnamese banking is functional domestically but limited internationally.</li><li><strong>Tax efficiency at scale</strong>. Singapore CIT is 17% (with SUTE for the first 3 YAs); Vietnam CIT is 20%. The Vietnam-Singapore Double Tax Agreement (DTA) eliminates dividend WHT in many cases. Capital gains in Singapore are not taxed at all.</li><li><strong>Operational ease</strong>. Setup is 1-3 business days. Annual compliance is straightforward. Currency moves freely. Hiring is simpler.</li></ul>",
             ]),
            ("Two structures Vietnamese founders typically use",
             [
                 "<strong>Structure A: Singapore HoldCo over Vietnam OpCo (most common).</strong> You incorporate a Singapore Pte Ltd that holds 100% of your Vietnamese LLC. Foreign investment registration with the Department of Planning and Investment in Vietnam is required for the holding structure. The Singapore HoldCo raises capital, holds IP, manages international expansion. The Vietnamese OpCo runs the Vietnam business.",
                 "<strong>Structure B: Singapore as the operating company (when most revenue is non-Vietnam).</strong> If your customers are international and your Vietnamese presence is just R&D or back-office, the Singapore Pte Ltd can be the primary operating entity. The Vietnam side becomes a service-provider subsidiary or even an employer-of-record arrangement.",
                 "<strong>Structure C: Pure Singapore entity (Vietnam-resident founder, no Vietnam operations).</strong> Some founders incorporate a Singapore Pte Ltd while remaining Vietnam tax-resident, with no Vietnamese subsidiary. This works for digital products serving global customers - but requires careful management of the Vietnamese tax authority's view (more on this below).",
             ]),
            ("State Bank of Vietnam (SBV) and outward investment",
             [
                 "Here is the most important piece many guides skip: <strong>Vietnam restricts the outward flow of capital to fund foreign investments.</strong> Sending money from Vietnam to fund a Singapore Pte Ltd's share capital requires SBV approval for outward investment registration.",
                 "Practical implications:",
                 "<ul><li>For most early-stage founders, the cleanest path is to <strong>fund the Singapore entity from non-Vietnamese sources</strong>. International salary, foreign clients paying in USD/SGD into a Singapore bank account, angel/VC funding raised internationally - all of these can capitalise the Singapore entity without needing SBV outward investment approval.</li><li>If the Singapore entity will hold the Vietnamese OpCo, the OpCo's operating profits can flow to Singapore as dividends (subject to the DTA - see below). This is a cleaner repatriation route than reverse-funding from Vietnam.</li><li>For founders who do need to send capital from Vietnam to Singapore, work with a Vietnamese FX-licensed bank and your Vietnamese counsel on the SBV outward investment registration. It's possible but adds 2-6 months to your timeline.</li></ul>",
                 "<strong>The pragmatic playbook:</strong> Many Vietnamese founders incorporate the Singapore entity with minimal initial capital (S$1 paid up), fund it through international revenue or external investment, and only later restructure if they need Vietnam-sourced capital to flow upward.",
             ]),
            ("Vietnam-Singapore Double Tax Agreement (DTA)",
             [
                 "The Vietnam-Singapore DTA (signed 1994, amended 2013) eliminates double taxation on income flowing between the two countries. Key features for founders:",
                 "<ul><li><strong>Dividends</strong>: 5% Vietnamese WHT on dividends paid from Vietnam OpCo to Singapore HoldCo, provided the Singapore company holds at least 50% of the Vietnamese company. 7% if holding is between 25-50%. 12.5% otherwise. All credited against any Singapore tax (which is typically zero on foreign dividends due to FSIE).</li><li><strong>Interest</strong>: 10% Vietnamese WHT on interest payments. Important if your Singapore HoldCo lends to the Vietnamese OpCo.</li><li><strong>Royalties</strong>: 5% on royalties for use of patents, designs, processes; 15% for trademark or experience-based royalties.</li><li><strong>Capital gains</strong>: Generally not taxed in either jurisdiction on share sales (Singapore has no capital gains tax; Vietnam has specific rules but the DTA limits double taxation).</li></ul>",
                 "<strong>Foreign-Sourced Income Exemption (FSIE)</strong>: Singapore exempts most foreign dividend income from Singapore tax if (a) the dividend has been subject to tax in the source country (the Vietnamese WHT counts), and (b) the foreign tax rate is at least 15%. Vietnam's headline 20% rate satisfies this. So the practical effective tax: 5% Vietnamese WHT on dividends, then no further Singapore tax.",
             ]),
            ("Banking pathways for Vietnamese founders",
             [
                 "Singapore banking for Vietnamese founders has both fast and slow paths:",
                 "<strong>Fast path (3-7 business days, fully remote):</strong>",
                 "<ul><li><strong>Aspire</strong> - business account with multi-currency support, Visa debit card, payment infrastructure. Most Karman Vietnamese clients start here.</li><li><strong>Wise Business</strong> - excellent for SGD/USD/EUR/GBP/VND multi-currency. Lower cost FX than traditional banks.</li><li><strong>StraitsX</strong> - good for crypto and stablecoin treasury (relevant for some Web3 founders).</li></ul>",
                 "<strong>Slower path (4-12 weeks, may require visit):</strong>",
                 "<ul><li><strong>DBS</strong> - traditional banking relationship, broader services, but slower onboarding and may require in-person visit.</li><li><strong>OCBC, UOB</strong> - similar to DBS in terms of process and timeline.</li><li><strong>HSBC</strong> - useful if you have existing HSBC relationship in Vietnam.</li></ul>",
                 "<strong>What banks ask for</strong>: Vietnamese passport (with EP if relocating), Vietnamese national ID, proof of Vietnam residential address, source of funds documentation (especially if seeding the Singapore account from Vietnam), and a clear business description. Karman's incorporation service includes bank introductions to streamline this.",
             ]),
            ("Employment Pass and relocation",
             [
                 "If you plan to relocate to Singapore as a founder, the Employment Pass (EP) is the main route. Key thresholds for Vietnamese founders in 2026:",
                 "<ul><li><strong>EP minimum salary</strong>: S$5,600/month general, S$6,200/month financial services (from January 2026)</li><li><strong>COMPASS framework</strong>: 40-point pass mark across salary, qualifications, diversity, and support for locals. <a href=\"/blog/compass-framework-2026-ep-renewal\">See our COMPASS 2026 guide</a>.</li><li><strong>Tech.Pass</strong>: Sponsor-free for senior tech professionals (US$20K+ monthly salary OR 5+ years at a leading tech company OR a product with 100K+ users). Renewable for 2 years without an employer.</li><li><strong>ONE Pass</strong>: For top-tier professionals at S$30K+ monthly salary. 5-year duration.</li></ul>",
                 "<strong>If you don't relocate</strong>: Karman provides nominee director services (from S$2,400/year) so you can incorporate the Singapore Pte Ltd without an EP. Many Vietnamese founders run the company remotely from Vietnam for the first 12-24 months, then relocate as the business scales.",
             ]),
            ("Tax residency for the Vietnamese founder personally",
             [
                 "If you remain Vietnam tax-resident (i.e., you don't relocate to Singapore), you remain liable for Vietnamese personal tax on your worldwide income. This includes salary from your Singapore Pte Ltd and potentially dividends.",
                 "If you relocate to Singapore on an EP and spend 183+ days in Singapore in a calendar year, you become Singapore tax-resident. At that point Vietnam may continue to claim tax residency under their domestic rules - which is where the DTA's <strong>tie-breaker rules</strong> come into play (permanent home, centre of vital interests, habitual abode, nationality).",
                 "<strong>Practical advice</strong>: This is a fact-specific area where general guidance falls short. Karman's tax team can run a residency analysis with your Vietnamese counsel to determine optimal timing and structuring.",
             ]),
            ("Common pitfalls for Vietnamese founders",
             [
                 "<strong>Pitfall 1: Funding the Singapore entity from Vietnam without SBV approval.</strong> This can create problems with both Vietnamese authorities and the Singapore bank's source-of-funds review. Use international sources where possible.",
                 "<strong>Pitfall 2: Not registering the foreign investment with Vietnamese authorities.</strong> If your Singapore HoldCo holds a Vietnamese OpCo, the Vietnamese authorities require foreign investment registration. Skipping this can invalidate the OpCo's foreign-ownership status.",
                 "<strong>Pitfall 3: Treating Singapore as a tax-shelter while remaining Vietnam-resident.</strong> Vietnam taxes worldwide income for tax residents. If you're using Singapore to defer or avoid Vietnamese tax without genuine substance in Singapore, expect challenge by the Vietnamese tax authority.",
                 "<strong>Pitfall 4: Setting up the Singapore entity before establishing real Singapore presence (when residency matters).</strong> If you eventually want to be Singapore tax-resident, begin spending time in Singapore, opening a Singapore bank account in your name, and securing housing - well before the year you want residency to apply.",
             ]),
            ("How Karman supports Vietnamese founders",
             [
                 "Karman has supported Vietnamese founders through ACRA incorporation, EP applications, banking introductions (Aspire, DBS), VCC fund administration for Vietnam-focused funds, and tax residency planning. We work alongside your Vietnamese counsel on the SBV outward investment piece where relevant.",
                 'Free tools that help: <a href="/tools/eligibility-checker">Eligibility Checker</a>, <a href="/tools/business-structure-recommender">Business Structure Recommender</a>, and the <a href="/tools/cost-calculator">Cost Calculator</a> with a Vietnam-specific filter for nominee director and EP planning.',
             ]),
        ],
        "faqs": [
            ("Can a Vietnamese founder incorporate a Singapore Pte Ltd remotely?",
             "Yes - the entire incorporation can be done remotely with Karman. You'll need a passport copy, Vietnamese national ID, proof of address, and source-of-funds documentation. ACRA approval is typically 1-3 business days. You'll need at least one ordinary resident director, which Karman provides as a nominee director service if you haven't yet secured your own EP."),
            ("Do I need approval from Vietnamese authorities to set up a Singapore company?",
             "It depends on the structure. If you're funding the Singapore entity with Vietnamese capital that flows out of Vietnam, the State Bank of Vietnam requires outward investment registration. If you're funding from international sources (foreign clients, foreign investment, international salary), no SBV approval is needed for the Singapore incorporation itself. If your Singapore entity will own a Vietnamese subsidiary, foreign investment registration with Vietnamese authorities is required for the Vietnamese subsidiary."),
            ("How does the Vietnam-Singapore DTA affect dividend flows?",
             "Dividends from a Vietnamese subsidiary to a Singapore parent are subject to 5% Vietnamese withholding tax if the Singapore parent holds at least 50% of the subsidiary, 7% for 25-50% ownership, and 12.5% otherwise. The Singapore parent typically pays no further tax on these dividends due to the Foreign-Sourced Income Exemption (FSIE), provided the dividends have been subject to tax in Vietnam (the WHT counts) and Vietnam's headline tax rate is at least 15% (it is - 20%)."),
            ("What's the cost of incorporating in Singapore as a Vietnamese founder?",
             "Karman's foreign founder incorporation package starts at S$2,800 and includes ACRA filing, nominee director (one year), corporate secretary, registered address, and constitution drafting. Add S$480/year for ongoing corporate secretary, S$2,400/year for ongoing nominee director, and accounting + GST + tax filing as needed. Use the <a href='/tools/cost-calculator'>Cost Calculator</a> for a precise quote based on your situation."),
            ("Can I be a Singapore Pte Ltd director without leaving Vietnam?",
             "Yes - you can be a director of a Singapore Pte Ltd while resident in Vietnam. You don't need an Employment Pass to be a director (only to be employed by the company). However, every Singapore Pte Ltd needs at least one ordinary resident director (Singapore Citizen, PR, or EP holder). If you don't have one, Karman provides nominee director services from S$2,400/year while you decide whether to relocate."),
        ],
        "sources": [
            ("https://www.iras.gov.sg/taxes/international-tax/dta", "IRAS - Avoidance of Double Taxation Agreements"),
            ("https://www.acra.gov.sg/how-to-guides/setting-up-a-private-limited-company", "ACRA - Setting Up a Private Limited Company"),
            ("https://www.mom.gov.sg/passes-and-permits/employment-pass", "MOM - Employment Pass"),
            ("https://www.sbv.gov.vn", "State Bank of Vietnam"),
        ],
        "related": [
            ("singapore-company-incorporation-indonesian-founders", "Foreign Founders", "guide", "Singapore Incorporation for Indonesian Founders", "Banking, FX, BKPM rules, and the Indonesia-Singapore DTA.", "10 min read"),
            ("singapore-company-incorporation-indian-founders", "Foreign Founders", "guide", "Singapore Incorporation for Indian Founders", "DTAA, FEMA/RBI, and structures like the flip and holding company.", "10 min read"),
            ("how-to-incorporate-company-singapore-foreigner", "Foreign Founders", "guide", "How to Incorporate in Singapore as a Foreigner", "End-to-end process: KYC, ACRA, banking, and timeline.", "9 min read"),
        ],
    },
]


# ============================================================================
# RENDERERS
# ============================================================================

def article_ldjson(blog):
    canonical = f"https://karman.com.sg/blog/{blog['slug']}"
    iso_date = f"{PUB_DATE}T00:00:00+08:00"
    faqs = [
        {
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {"@type": "Answer", "text": a},
        }
        for (q, a) in blog["faqs"]
    ]
    return {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Article",
                "headline": blog["title"],
                "url": canonical,
                "image": "https://karman.com.sg/og-image.png",
                "datePublished": iso_date,
                "dateModified": iso_date,
                "author": {"@type": "Organization", "name": "Karman Editorial Team", "url": "https://karman.com.sg"},
                "publisher": {
                    "@type": "Organization",
                    "name": "Karman Corporate Services",
                    "url": "https://karman.com.sg",
                    "logo": {"@type": "ImageObject", "url": "https://karman.com.sg/og-image.png"},
                },
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://karman.com.sg/"},
                    {"@type": "ListItem", "position": 2, "name": "Blog", "item": "https://karman.com.sg/blog/"},
                    {"@type": "ListItem", "position": 3, "name": blog["breadcrumb_short"], "item": canonical},
                ],
            },
            {"@type": "FAQPage", "mainEntity": faqs},
        ],
    }


def render_sections(sections):
    parts = []
    for (heading, paragraphs) in sections:
        parts.append(f"      <h2>{esc(heading)}</h2>\n")
        for p in paragraphs:
            if p.strip().startswith("<"):
                parts.append(f"      {p}\n")
            else:
                parts.append(f"      <p>{p}</p>\n")
    return "".join(parts)


def render_faqs(faqs):
    parts = []
    for (q, a) in faqs:
        parts.append(f'''      <div class="faq-item">
        <button class="faq-question" aria-expanded="false">{esc(q)}<span class="faq-icon">+</span></button>
        <div class="faq-answer"><p>{esc(a)}</p></div>
      </div>
''')
    return "".join(parts)


def render_sources(sources):
    parts = []
    for (url, title) in sources:
        parts.append(f'      <li><a href="{esc(url)}" target="_blank" rel="noopener noreferrer">{esc(title)} ↗</a></li>\n')
    return "".join(parts)


def render_related(related):
    parts = []
    for (slug, tag, tag_class, title, excerpt, read) in related:
        parts.append(f'''        <a href="/blog/{slug}" class="blog-card">
          <span class="blog-card__tag blog-card__tag--{tag_class}">{esc(tag)}</span>
          <h3 class="blog-card__title">{esc(title)}</h3>
          <p class="blog-card__excerpt">{esc(excerpt)}</p>
          <div class="blog-card__meta"><span>{read}</span></div>
        </a>
''')
    return "".join(parts)


def render_blog(blog):
    canonical = f"https://karman.com.sg/blog/{blog['slug']}"
    ld = article_ldjson(blog)
    pretty_date = "May 2026"

    return f"""<!DOCTYPE html>
<html lang="en-SG">
<head>
  <!-- Google tag (gtag.js) -->
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', 'G-DVKN5K8KSD');
    (function(){{
      var loaded = false;
      function loadGTM(){{
        if (loaded) return;
        loaded = true;
        var s = document.createElement('script');
        s.async = true;
        s.src = 'https://www.googletagmanager.com/gtag/js?id=G-DVKN5K8KSD';
        document.head.appendChild(s);
      }}
      var events = ['scroll','keydown','mousemove','touchstart','click'];
      function trigger(){{ events.forEach(function(e){{ window.removeEventListener(e, trigger, {{passive:true}}); }}); loadGTM(); }}
      events.forEach(function(e){{ window.addEventListener(e, trigger, {{passive:true, once:true}}); }});
      setTimeout(loadGTM, 5000);
    }})();
  </script>

  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <link rel="icon" type="image/png" href="/favicon.png" />
  <title>{esc(blog['title'])} | Karman</title>
  <meta name="description" content="{esc(blog['description'])}" />
  <meta name="robots" content="index, follow" />
  <link rel="canonical" href="{canonical}" />

  <meta property="og:type" content="article" />
  <meta property="og:url" content="{canonical}" />
  <meta property="og:title" content="{esc(blog['title'])}" />
  <meta property="og:description" content="{esc(blog['description'])}" />
  <meta property="og:image" content="https://karman.com.sg/og-image.png" />
  <meta name="twitter:card" content="summary_large_image" />

  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Sora:wght@400;600;700;800&display=swap" />
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Sora:wght@400;600;700;800&display=swap" media="print" onload="this.media='all'" />
  <noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Sora:wght@400;600;700;800&display=swap" /></noscript>
  <style>{STYLES_CSS_INLINE}</style>
  <link rel="stylesheet" href="../../tools.css" />
  <link rel="stylesheet" href="../../blog.css" />

  <script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False, indent=2)}
  </script>
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "WebPage",
    "speakable": {{
      "@type": "SpeakableSpecification",
      "cssSelector": ["h1", ".article-body > p:first-child", ".article-faq-section .faq-answer p"]
    }}
  }}
  </script>
</head>
<body class="article-page-layout">

{HEADER_HTML}
  <section class="article-hero">
    <div class="container">
      <nav class="article-breadcrumb" aria-label="Breadcrumb">
        <a href="/">Home</a><span>›</span>
        <a href="/blog">Blog</a><span>›</span>
        <span>{esc(blog['breadcrumb_short'])}</span>
      </nav>
      <span class="article-hero__tag">{esc(blog['tag'])}</span>
      <h1>{esc(blog['title'])}</h1>
      <div class="article-hero__meta">
        <span class="article-hero__meta-item">📅 {pretty_date}</span>
        <span class="article-hero__meta-dot"></span>
        <span class="article-hero__meta-item">⏱ {blog['read_min']} min read</span>
        <span class="article-hero__meta-dot"></span>
        <span class="article-hero__meta-item">✍️ Karman Editorial Team</span>
      </div>
    </div>
  </section>

  <div class="article-layout">

    <article class="article-body">

      <p>{blog['lede']}</p>

      <p>{blog['intro_p2']}</p>

{render_sections(blog['sections'])}
      <section class="article-sources-section" style="margin-top:40px;padding-top:28px;border-top:1px solid var(--gray-200);">
        <h3 style="font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:var(--gray-500);margin-bottom:12px;">Official Sources</h3>
        <ul style="list-style:none;display:flex;flex-direction:column;gap:6px;">
{render_sources(blog['sources'])}        </ul>
      </section>

      <section class="article-faq-section" style="margin-top:56px;padding-top:0;">
        <h2>Frequently Asked Questions</h2>
        <div class="faq__grid" style="max-width:100%;margin-top:24px;">
{render_faqs(blog['faqs'])}        </div>
      </section>

    </article>

    <aside class="article-sidebar">
      <div class="sidebar-cta">
        <div class="sidebar-cta__eyebrow">Ready to incorporate?</div>
        <h3>Get started from S$699</h3>
        <p>Karman handles name check, ACRA filing, nominee director, and company secretary. Most applications approved within 1 business day.</p>
        <a href="/onboarding" class="btn btn--primary">Start your application →</a>
        <a href="/tools" class="sidebar-cta__secondary">Try our free tools first</a>
      </div>
      <div class="sidebar-tools">
        <h4>Useful free tools</h4>
        <a href="/tools/cost-calculator">
          <span>🧮</span><span>Cost Calculator</span>
        </a>
        <a href="/tools/business-structure-recommender">
          <span>🏗️</span><span>Structure Recommender</span>
        </a>
        <a href="/tools/eligibility-checker">
          <span>✅</span><span>Eligibility Checker</span>
        </a>
      </div>
    </aside>

  </div>

  <section class="article-related">
    <div class="container">
      <h2 class="article-related__heading">Related articles</h2>
      <div class="article-related__grid">
{render_related(blog['related'])}      </div>
    </div>
  </section>

{FOOTER_HTML}
  <script src="/script.js"></script>

<script src="https://unpkg.com/lucide@latest"></script><script>lucide.createIcons();</script></body>
</html>
"""


def main():
    for blog in BLOGS:
        d = BLOG_DIR / blog["slug"]
        d.mkdir(exist_ok=True)
        (d / "index.html").write_text(render_blog(blog), encoding="utf-8")
        print(f"Wrote {d / 'index.html'}")
    print(f"\nGenerated {len(BLOGS)} blog posts.")


if __name__ == "__main__":
    main()
