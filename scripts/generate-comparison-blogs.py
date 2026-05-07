#!/usr/bin/env python3
"""Generate 3 comparison blog posts under /blog/<slug>/index.html.

Comparisons:
1. Singapore vs Hong Kong post-2026 NSL
2. Singapore Pte Ltd vs Delaware C-Corp
3. Singapore VCC vs Mauritius GBC for India funds
"""

import json
import html as htmlmod
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BLOG_DIR = ROOT / "blog"

PUB_DATE = "2026-05-07"


def esc(s):
    return htmlmod.escape(s, quote=True) if s else ""


HEADER_HTML = """  <header class="header" id="header">
    <nav class="nav container" aria-label="Main navigation">
      <a href="/" class="nav__logo"><img src="/logo.svg" alt="Karman" class="nav__logo-img"></a>
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
          <a href="/" class="nav__logo"><img src="/logo.svg" alt="Karman" class="nav__logo-img"></a>
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
    # 1. Singapore vs Hong Kong post-2026 NSL
    # ------------------------------------------------------------------
    {
        "slug": "singapore-vs-hong-kong-2026",
        "title": "Singapore vs Hong Kong 2026: Which Is Better for Founders Now?",
        "description": "Tax, banking, talent, political risk, capital controls, and the post-NSL reality. The honest 2026 comparison for founders choosing between Singapore and Hong Kong.",
        "keyword": "singapore vs hong kong 2026",
        "tag": "Comparison",
        "tag_class": "guide",
        "breadcrumb_short": "Singapore vs Hong Kong",
        "read_min": 12,
        "lede": "<strong>For most founders in 2026, Singapore is the clear default; Hong Kong only makes sense for businesses with deep China-mainland exposure.</strong> The two jurisdictions used to be near-substitutes - both common-law, low-tax, English-speaking financial hubs. Since the 2020 National Security Law (NSL), the 2024 Article 23 legislation, and capital control tightening on outbound flows from mainland China, the gap has widened materially. This is the no-marketing, side-by-side comparison founders actually need.",
        "intro_p2": "We cover effective tax rates, banking access, capital movement, talent visas, political and rule-of-law risk, listing routes, and the specific founder profiles that still pick Hong Kong over Singapore.",
        "sections": [
            ("The headline comparison",
             [
                 '<div class="table-wrap"><table><thead><tr><th>Factor</th><th>Singapore</th><th>Hong Kong</th></tr></thead><tbody>'
                 '<tr><td>Headline corporate tax</td><td>17%</td><td>16.5% (8.25% on first HK$2M profit)</td></tr>'
                 '<tr><td>Effective tax (small profits)</td><td>~4-8% with SUTE/PTE schemes</td><td>~8.25% under two-tier rate</td></tr>'
                 '<tr><td>Capital gains tax</td><td>None</td><td>None</td></tr>'
                 '<tr><td>Dividend WHT (paid out)</td><td>0%</td><td>0%</td></tr>'
                 '<tr><td>Personal income tax (top)</td><td>24% (above S$1M)</td><td>17% (salaries tax cap) / 15% (standard rate)</td></tr>'
                 '<tr><td>GST/VAT</td><td>9% GST</td><td>None</td></tr>'
                 '<tr><td>Banking access for foreign founders</td><td>Generally good (DBS, OCBC, UOB, Aspire, Wise)</td><td>Tighter post-2020; smaller banks more selective</td></tr>'
                 '<tr><td>Capital controls</td><td>None</td><td>None on HK side; mainland CNY flows restricted</td></tr>'
                 '<tr><td>Rule-of-law independence</td><td>High (apex court is local SC)</td><td>Eroding (NSL cases bypass jury, NPCSC interpretation)</td></tr>'
                 '<tr><td>Press freedom rank (RSF 2025)</td><td>~125</td><td>~140</td></tr>'
                 '<tr><td>Treaty network</td><td>~100 DTAs</td><td>~50 DTAs</td></tr>'
                 '<tr><td>Talent visa (founder)</td><td>EntrePass / EP S$5,600+</td><td>Top Talent Pass / IANG / QMAS</td></tr>'
                 '<tr><td>Time zone advantage</td><td>SGT (UTC+8) - covers India, MENA, ASEAN</td><td>HKT (UTC+8) - covers mainland China</td></tr>'
                 '<tr><td>Listing route</td><td>SGX (smaller) + dual-listing routes</td><td>HKEX (large, China-linked)</td></tr>'
                 '</tbody></table></div>',
                 "On almost every metric except listing access to mainland China capital, Singapore is at parity or ahead in 2026. The one structural advantage Hong Kong retains - direct integration with Greater Bay Area / mainland markets - is the entire reason to still pick it.",
             ]),
            ("Tax: the real numbers",
             [
                 "<strong>Singapore.</strong> Headline rate is 17%. Most early-stage founders pay materially less:",
                 "<ul><li><strong>Startup Tax Exemption (SUTE):</strong> First S$100,000 of normal chargeable income is 75% exempt; next S$100,000 is 50% exempt. Available for the first 3 YAs of a new tax-resident company. <a href=\"/glossary/sute\">Full rules in our glossary</a>.</li><li><strong>Partial Tax Exemption (PTE):</strong> After SUTE expires, first S$10,000 is 75% exempt and next S$190,000 is 50% exempt. Permanent.</li><li><strong>Budget 2026 CIT rebate:</strong> 40% rebate on YA 2026 tax payable, capped at S$30,000. Applies to all active companies.</li></ul>",
                 "Translated: a profitable Year-1 startup with S$300K profit pays roughly S$14,500 in CIT after SUTE and the 2026 rebate - an effective rate of ~4.8%.",
                 "<strong>Hong Kong.</strong> Two-tier rate: 8.25% on the first HK$2 million of assessable profits, 16.5% above that. No general SUTE-equivalent. For a similar S$300K profit (≈HK$1.75M), you pay ~HK$144,375 - roughly S$24,500. Effective rate ~8.2%.",
                 "<strong>Verdict on tax:</strong> Singapore is meaningfully cheaper for early-stage profitable companies; broadly equivalent for mature businesses (both at ~16.5-17%). The Singapore advantage compounds with the Enterprise Innovation Scheme (400% deduction on qualifying AI/R&D spend) which has no clean Hong Kong equivalent.",
             ]),
            ("Banking: this is where Hong Kong actually lost",
             [
                 "Pre-2020, opening a Hong Kong corporate account was easier than Singapore for many founder profiles. That's no longer true.",
                 "<strong>Hong Kong banking now:</strong>",
                 "<ul><li>Major banks (HSBC, Standard Chartered, BOC HK) have tightened KYC for new accounts, particularly for non-resident-controlled entities</li><li>Account opening typically requires director travel to Hong Kong, source-of-funds documentation, and detailed business plans</li><li>Several second-tier banks have dramatically reduced their non-resident SME books</li><li>Closure of accounts for founders with mainland China political exposure is now routine</li><li>Fintech alternatives (Aspire, Wise) have lighter Hong Kong presence than Singapore</li></ul>",
                 "<strong>Singapore banking now:</strong>",
                 "<ul><li>DBS, OCBC, UOB still open accounts for foreign-owned Pte Ltds with proper documentation, including remote/video onboarding for many profiles</li><li>Aspire, Wise, Airwallex have full Singapore product suites</li><li>Account opening typically 1-3 weeks; in-person presence often optional</li><li>MAS regulatory clarity is high - banks know exactly what compliance posture they need to maintain</li></ul>",
                 "For founders without a Greater China nexus, Singapore banking is meaningfully easier in 2026.",
             ]),
            ("The post-NSL legal and political risk",
             [
                 "Three legal events have changed Hong Kong's risk profile:",
                 "<ol><li><strong>National Security Law (June 2020):</strong> Imposed by Beijing's NPCSC, criminalising secession, subversion, terrorism, and collusion with foreign forces. Cases under NSL can be tried without jury, and prosecutors can apply to bypass standard bail provisions.</li><li><strong>Article 23 (March 2024):</strong> Hong Kong's domestic security legislation, expanding NSL with offences around 'external interference', state secrets, and treason. Significantly broader and more ambiguous than NSL.</li><li><strong>NPCSC interpretation power:</strong> Beijing's Standing Committee retains the power to issue authoritative interpretations of Hong Kong law, including the Basic Law. This has been used multiple times to override Hong Kong court rulings.</li></ol>",
                 "<strong>What this means for founders:</strong>",
                 "<ul><li>The probability of arbitrary application of these laws to ordinary commercial activity remains low - but the worst-case scenario (asset freeze, exit ban for directors, secret detention) now exists in a way it didn't pre-2020</li><li>Several global law firms have downsized their Hong Kong dispute practices specifically because contractual disputes with mainland counterparties have become harder to predict</li><li>International arbitration in Hong Kong is still respected, but venue clauses are increasingly drafted to specify Singapore (SIAC) as the seat</li><li>Outbound capital flow from mainland-controlled entities through Hong Kong is now substantially restricted - this matters if your business model assumed easy CNY-out</li></ul>",
                 "<strong>Singapore's position:</strong> The Singapore International Arbitration Centre (SIAC) has overtaken HKIAC in many league tables for Asia-seated arbitrations since 2020. The Singapore International Commercial Court (SICC) hears international disputes with foreign judges. Rule-of-law independence is high; the apex court is the Singapore Court of Appeal, with no external interpretation authority.",
             ]),
            ("Talent visas and labour mobility",
             [
                 "<strong>Singapore.</strong>",
                 "<ul><li><strong>Employment Pass (EP):</strong> Minimum salary S$5,600/month (S$6,200 in financial services) from January 2026. Must score at least 40 points under <a href=\"/blog/compass-framework-2026-ep-renewal\">COMPASS</a>.</li><li><strong>EntrePass:</strong> For founders launching innovative startups. Minimum S$50K paid-up capital, business plan, qualifying entrepreneurial criteria.</li><li><strong>Tech.Pass / ONE Pass:</strong> For senior tech talent (S$30K+/month) and high-earners. Highly selective.</li><li><strong>Path to PR:</strong> Generally 2-5 years on EP for high-earners; longer for others.</li></ul>",
                 "<strong>Hong Kong.</strong>",
                 "<ul><li><strong>Top Talent Pass Scheme (TTPS):</strong> Three categories - high earners (HK$2.5M+ annual income previously), graduates of top-100 universities (last 5 years), or graduates of top-100 with 3+ years experience.</li><li><strong>General Employment Policy (GEP):</strong> No minimum salary in legislation, but typically requires a specialised role and salary commensurate with market.</li><li><strong>QMAS:</strong> Points-based for skilled professionals without a Hong Kong job offer. Quota system.</li><li><strong>IANG:</strong> For non-local graduates of Hong Kong universities.</li></ul>",
                 "<strong>Verdict:</strong> Hong Kong's TTPS is genuinely founder-friendly for graduates of top universities and is faster to obtain than Singapore EP for many profiles. Singapore has tighter qualitative screening but higher long-term predictability (PR pathway is more transparent). For founders relocating themselves and 1-2 senior hires, Singapore's process is more rigorous but the outcome more durable.",
             ]),
            ("Capital movement and structuring",
             [
                 "Both jurisdictions have no capital controls on the ground. The difference is what you can do with cross-border flows:",
                 "<strong>Singapore.</strong>",
                 "<ul><li>SGD freely convertible. No exchange controls.</li><li>~100 double tax agreements (DTAs) - including comprehensive treaties with India, China, USA, UK, Indonesia, Malaysia, Vietnam.</li><li>Withholding tax on dividends paid out: 0%. Interest: 15% (often reduced under DTA). Royalties: 10% (often reduced).</li><li>Tax-resident certificate (CoR) issued by IRAS unlocks DTA benefits.</li></ul>",
                 "<strong>Hong Kong.</strong>",
                 "<ul><li>HKD freely convertible. No exchange controls on Hong Kong side.</li><li>~50 DTAs - smaller network than Singapore. Notable gaps: no comprehensive DTA with USA, India treaty newer (2018) and less tested than Singapore-India DTA.</li><li>Withholding tax on dividends: 0%. Interest: 0%. Royalties: 4.95-16.5% depending on regime.</li><li>Mainland China outbound CNY flows are restricted by SAFE - Hong Kong proximity doesn't change this.</li></ul>",
                 "<strong>Founder takeaway:</strong> If your business has India, Indonesia, Vietnam, or Middle East flows, Singapore's treaty network is materially better. If your business is primarily mainland China inbound investment or licensing, Hong Kong has historical advantages but they're eroding.",
             ]),
            ("Listing and IPO routes",
             [
                 "<strong>Hong Kong (HKEX).</strong> Asia's largest exchange by total market cap when measured with mainland Chinese listings. Ideal for businesses with China revenue exposure - the investor base understands the market, multiples for China-themed names are typically higher than SGX.",
                 "<strong>Singapore (SGX).</strong> Smaller exchange. Stronger for REITs, business trusts, and ASEAN-themed names. Liquidity for sub-S$500M cap names is thin. Most Singapore-incorporated companies that IPO go to NYSE/NASDAQ via a redomicile structure (the 'Singapore parent + US ADR' route doesn't exist - you typically flip to a Cayman or Delaware top-co).",
                 "<strong>If you're aiming for US public markets:</strong> Singapore is the better operating base (treaty network, talent, ease of doing business) but you'll structure with Cayman/Delaware as the listing vehicle either way. Hong Kong vs Singapore choice has minimal impact on your US listing path.",
                 "<strong>If you're aiming for HKEX:</strong> Hong Kong incorporation simplifies the listing process. A Singapore Pte Ltd can also list on HKEX but typically restructures into a Cayman vehicle first.",
             ]),
            ("Who should still pick Hong Kong",
             [
                 "Despite everything above, Hong Kong remains the right choice for specific founder profiles:",
                 "<ul><li><strong>Mainland China revenue exposure:</strong> If your customer base, supply chain, or strategic partners are predominantly mainland Chinese, Hong Kong's mainland connectivity (CEPA preferences, Greater Bay Area access, RMB clearing) outweighs governance trade-offs</li><li><strong>HKEX listing in your 3-5 year roadmap:</strong> Cleaner path than restructuring later</li><li><strong>Existing Hong Kong banking and operations:</strong> The cost of relocating an established business may exceed the benefit</li><li><strong>Trade in goods physically routing through Hong Kong:</strong> Free port advantages for re-export, particularly electronics, watches, and luxury goods</li><li><strong>Insurance and reinsurance underwriting with mainland focus:</strong> Hong Kong's IA-licensed insurers have direct mainland market access that Singapore's MAS-licensed insurers don't</li></ul>",
                 "Outside these profiles, Singapore is the lower-friction default for new founders in 2026.",
             ]),
            ("How to make the call (decision framework)",
             [
                 "Walk through these questions in order:",
                 "<ol><li><strong>Is mainland China >40% of your revenue or supply chain?</strong> Yes → Hong Kong likely. No → continue.</li><li><strong>Is HKEX listing within your 5-year plan?</strong> Yes and serious → Hong Kong likely. No → continue.</li><li><strong>Do you need an India, Indonesia, Vietnam, MENA, or US treaty position?</strong> Yes → Singapore. No → continue.</li><li><strong>Are you comfortable with NPCSC interpretation power over your operating-jurisdiction's law?</strong> If no → Singapore.</li><li><strong>Can your founders/employees realistically pass Singapore EP / EntrePass?</strong> If no → consider Hong Kong TTPS or alternative jurisdictions.</li></ol>",
                 "Most founders working through this list end up with Singapore as the answer in 2026. The exceptions are well-defined and self-aware.",
             ]),
            ("How Karman handles this",
             [
                 'If you\'re evaluating Singapore: we incorporate Pte Ltds for global founders and run nominee director, accounting, GST, and corporate secretary services. Our <a href="/tools/business-structure-recommender">structure recommender</a> walks you through which Singapore vehicle (Pte Ltd, VCC, branch, RO) fits your facts.',
                 "If you decide on Hong Kong: we don't incorporate Hong Kong companies but we work with regional partners and can introduce you. We can still help with the Singapore side of dual-jurisdiction structures (e.g., Singapore Pte Ltd holding mainland-China operating subsidiary, with a Hong Kong intermediary for licensing).",
             ]),
        ],
        "faqs": [
            ("Is it harder to get a Singapore Pte Ltd than a Hong Kong Limited?",
             "No. Both jurisdictions have efficient corporate registries. Singapore (ACRA) approves most incorporations within 1 business day; Hong Kong (CR) typically 1-2 days. Document requirements are similar. Where Singapore can be more involved is in nominee director sourcing and bank account opening for foreign founders, but with a registered filing agent like Karman, the process is straightforward."),
            ("Can I move my Hong Kong company to Singapore?",
             "Yes, via inward redomiciliation. Singapore allows foreign companies to redomicile as a Singapore Pte Ltd while preserving the original entity, contracts, and tax history. The Hong Kong company applies for de-registration in Hong Kong concurrently. The process takes 6-12 weeks and requires meeting Singapore's substance requirements."),
            ("Does Singapore tax my worldwide income like the US does?",
             "No. Singapore taxes on a territorial basis - foreign-sourced income is generally not taxed unless remitted to Singapore. Hong Kong is similar (territorial source principle). Both are dramatically more favourable than the US worldwide system."),
            ("Will my Hong Kong bank account be closed if I move to Singapore?",
             "Not automatically. Banks close accounts for risk-management reasons, not because you opened a Singapore account. However, if you're winding down Hong Kong operations entirely, banks may eventually close inactive accounts. Maintain documentation if you want to keep the account active for future use."),
            ("Is Hong Kong still useful as a holding company jurisdiction for international groups?",
             "Less than it used to be. The combination of NSL/Article 23 risk, narrower DTA network, and tighter banking has shifted regional holding company structuring toward Singapore. Singapore Pte Ltds and VCCs now host the regional holding tier for most new structures we see being set up in 2025-2026."),
        ],
        "sources": [
            ("https://www.iras.gov.sg/taxes/corporate-income-tax/basics-of-corporate-income-tax/corporate-income-tax-rate-rebates-tax-exemption-schemes",
             "IRAS - Corporate Income Tax Rates"),
            ("https://www.ird.gov.hk/eng/tax/bus_pft.htm", "Hong Kong IRD - Profits Tax"),
            ("https://www.mom.gov.sg/passes-and-permits/employment-pass/eligibility",
             "MOM - Employment Pass Eligibility"),
            ("https://www.elegislation.gov.hk/hk/A406", "Hong Kong - Safeguarding National Security Ordinance (Article 23)"),
        ],
        "related": [
            ("singapore-vs-delaware-c-corp-2026", "Comparison", "guide", "Singapore Pte Ltd vs Delaware C-Corp (2026)",
             "Tax, banking, ESOP, fundraising, and the structures VCs actually accept.", "12 min read"),
            ("singapore-flip-structure-indian-startups", "Indian Founders", "guide",
             "Singapore Flip Structure for Indian Startups",
             "How to flip your Indian startup to a Singapore holding company. FEMA, ODI, LRS, POEM.", "11 min read"),
            ("oecd-pillar-two-singapore-holding-company", "Tax", "tax",
             "OECD Pillar Two and Your Singapore Holding Company",
             "What the 15% global minimum tax means for Singapore-structured groups.", "9 min read"),
        ],
    },

    # ------------------------------------------------------------------
    # 2. Singapore Pte Ltd vs Delaware C-Corp
    # ------------------------------------------------------------------
    {
        "slug": "singapore-vs-delaware-c-corp-2026",
        "title": "Singapore Pte Ltd vs Delaware C-Corp: Founder's Decision Guide 2026",
        "description": "Tax, ESOP, fundraising, banking, and what VCs actually accept. The honest comparison between Singapore Pte Ltd and Delaware C-Corp for global founders in 2026.",
        "keyword": "singapore pte ltd vs delaware c-corp",
        "tag": "Comparison",
        "tag_class": "guide",
        "breadcrumb_short": "Singapore vs Delaware",
        "read_min": 12,
        "lede": "<strong>If your customers are global and you're not yet committed to a US fundraise, incorporate as a Singapore Pte Ltd. If you're chasing Silicon Valley VC dollars, you need a Delaware C-Corp - or you'll need to flip later.</strong> The two structures serve different optimisation goals: Singapore minimises tax and operational friction; Delaware maximises compatibility with US venture capital. This piece covers what each is, what they cost, and how the decision actually plays out for typical founder profiles.",
        "intro_p2": "We work through tax, fundraising, ESOP mechanics, banking, governance, and the specific founder situations where each structure wins. We'll also show you the cost and timeline of flipping between them if you change your mind.",
        "sections": [
            ("Headline comparison",
             [
                 '<div class="table-wrap"><table><thead><tr><th>Factor</th><th>Singapore Pte Ltd</th><th>Delaware C-Corp</th></tr></thead><tbody>'
                 '<tr><td>Headline corporate tax</td><td>17%</td><td>21% federal + ~0% Delaware state (if no DE operations)</td></tr>'
                 '<tr><td>Effective tax (small profits)</td><td>~4-8% with SUTE/PTE</td><td>~21% (no startup exemption)</td></tr>'
                 '<tr><td>Capital gains tax (company level)</td><td>None on most gains</td><td>21% (federal LTCG rolled into corporate rate)</td></tr>'
                 '<tr><td>Capital gains tax (shareholder)</td><td>None for individual founders</td><td>15-20% federal + state</td></tr>'
                 '<tr><td>Dividend WHT to non-residents</td><td>0%</td><td>30% (often 5-15% under treaty)</td></tr>'
                 '<tr><td>QSBS Section 1202 exclusion</td><td>N/A</td><td>Up to $10M gain exclusion (5-year hold)</td></tr>'
                 '<tr><td>Setup cost</td><td>S$699-S$1,500 incl. nominee + secretary</td><td>$300-$1,000 + EIN + agent + Section 351</td></tr>'
                 '<tr><td>Annual compliance cost</td><td>S$1,200-S$3,000</td><td>$2,500-$8,000 (CPA + DE franchise tax)</td></tr>'
                 '<tr><td>Director residency</td><td>1 ordinarily resident director required</td><td>None</td></tr>'
                 '<tr><td>Founder visa pathway</td><td>EP / EntrePass / Tech.Pass</td><td>O-1 / E-2 / L-1 (no startup-specific visa)</td></tr>'
                 '<tr><td>VC familiarity (US VCs)</td><td>Lower - many require flip to DE</td><td>Highest - native vehicle</td></tr>'
                 '<tr><td>VC familiarity (SE Asia/India VCs)</td><td>High - native vehicle</td><td>Acceptable but flip preferred eventually</td></tr>'
                 '<tr><td>ESOP grants</td><td>Stock options or share awards via Pte Ltd ESOP scheme</td><td>NSO/ISO grants under standard plans (409A required)</td></tr>'
                 '<tr><td>Liquidity event - acquisition by US co.</td><td>Smooth if structure is clean; cross-border tax planning needed</td><td>Native; QSBS may apply</td></tr>'
                 '<tr><td>Liquidity event - IPO</td><td>SGX (small) or flip to Cayman/Delaware for US IPO</td><td>Native NYSE/Nasdaq path</td></tr>'
                 '</tbody></table></div>',
                 "The single most decision-relevant row is fundraising. Everything else has workarounds; investor friction does not.",
             ]),
            ("The tax math (where Singapore wins)",
             [
                 "<strong>Singapore Pte Ltd, Year 1 with S$300K profit:</strong>",
                 "<ul><li>SUTE: First S$100K is 75% exempt (S$25K taxable), next S$100K is 50% exempt (S$50K taxable), rest is fully taxable (S$100K)</li><li>Chargeable income: S$175K. Tax at 17%: S$29,750.</li><li>40% Budget 2026 CIT rebate: -S$11,900</li><li><strong>Final tax: S$17,850 (5.95% effective rate)</strong></li></ul>",
                 "<strong>Delaware C-Corp, Year 1 with US$220K profit (≈S$300K):</strong>",
                 "<ul><li>No startup exemption equivalent</li><li>21% federal corporate tax: $46,200</li><li>Delaware franchise tax: ~$400-$2,000 depending on share structure</li><li><strong>Final tax: ~$46,600 (21.2% effective rate)</strong></li></ul>",
                 "On a like-for-like profit basis, Singapore is 3-4x cheaper at the company level for early-stage businesses. The gap narrows as profits scale (both jurisdictions converge to ~17-21% on big numbers) but remains material.",
                 "<strong>Where Delaware can win:</strong> If your company will never be profitable until exit (typical for VC-funded SaaS/AI startups), the corporate tax difference is moot. The relevant tax becomes the shareholder-level treatment at exit - and that's where Delaware's QSBS Section 1202 exclusion (up to $10M of gain federally exempt for qualifying small business stock held 5+ years by individual founders) is genuinely valuable for US-resident founders.",
             ]),
            ("Fundraising: the real decision driver",
             [
                 "<strong>Why US VCs strongly prefer Delaware C-Corps:</strong>",
                 "<ul><li>Standard fund LPs include LP-side restrictions on investing in foreign corporations - their tax structures may be incompatible with PFIC/CFC rules</li><li>Convertible notes, SAFEs, and standard preferred stock terms have decades of US case law - these instruments are well-understood, and lawyers can paper deals fast</li><li>Section 83(b) elections, 409A valuations, and ISO grants don't have clean equivalents in non-US jurisdictions</li><li>Board mechanics (delegated power, drag-along/tag-along provisions) under DGCL are predictable</li><li>Diligence becomes easier - lawyers know what to check</li></ul>",
                 "<strong>What this means in practice:</strong>",
                 "<ul><li>YC, Sequoia US, a16z, and most other US-based seed/Series A funds typically require Delaware before they'll wire</li><li>India- and SEA-based funds (Peak XV, Lightspeed Asia, Insignia, Vertex, B Capital) commonly invest into Singapore Pte Ltds without flip</li><li>Crossover funds and growth-stage US capital usually demand a flip before Series B/C</li></ul>",
                 "<strong>The flip option:</strong> You can incorporate as a Singapore Pte Ltd, raise from regional VCs at seed/pre-seed, then 'flip' to a Delaware top-co before US fundraising. The flip costs $25K-$50K in legal fees plus whatever tax exposure arises from gain recognition on the contributed Singapore shares. Most well-advised flips are designed to minimise this tax leakage.",
                 "<strong>Anti-pattern:</strong> Incorporating in Delaware before you have US revenue, US customers, or US fundraising commitments. The annual compliance cost ($2,500-$8,000) and US tax filing burden often outweigh the optionality of being 'VC-ready' for an event that may never happen.",
             ]),
            ("ESOP / employee equity",
             [
                 "<strong>Delaware C-Corp ESOP.</strong>",
                 "<ul><li>Standard NSO (Non-qualified Stock Options) and ISO (Incentive Stock Options) grants under approved equity plan</li><li>Requires Section 409A valuation annually (or at material events) - typical cost $1,000-$5,000</li><li>ISO grants offer favourable employee tax treatment if held 2 years from grant + 1 year from exercise</li><li>Section 83(b) elections allow founders/early employees to lock in capital gains treatment</li><li>Universal investor and employee familiarity</li></ul>",
                 "<strong>Singapore Pte Ltd ESOP.</strong>",
                 "<ul><li>Stock option scheme or share award scheme adopted by board resolution and shareholder approval</li><li>No Section 409A equivalent - simpler, but options must still be issued at fair market value to avoid IRAS gain-on-grant treatment</li><li>Employee tax: gain on exercise (FMV at exercise minus exercise price) is taxable as employment income at marginal rates</li><li>QESS (Qualified Employee Stock Scheme) provides up to S$1M lifetime exemption for employees of qualifying SMEs - meaningful tax benefit</li><li>Singapore-only employees: simple. Mixed Singapore + US employees: more complex (US employees of a non-US company face PFIC issues with options)</li></ul>",
                 "<strong>Verdict:</strong> If your team is primarily in Singapore/Asia, the Pte Ltd ESOP is cleaner and cheaper. If you'll have material US-resident employees, Delaware ESOP avoids cross-border employee tax complexity.",
             ]),
            ("Banking and operations",
             [
                 "<strong>Singapore.</strong> DBS, OCBC, UOB, Aspire, Wise, Airwallex all open accounts for foreign-owned Pte Ltds. Most account opening completes within 2-3 weeks. SGD is freely convertible. Multi-currency accounts are standard.",
                 "<strong>Delaware C-Corp.</strong> Without US presence (US address, US directors, US founders), opening a US bank account is genuinely difficult. Mercury, Brex, and Bluevine cater specifically to non-US-resident-owned Delaware C-Corps but require valid EIN, business documentation, and ITINs/SSNs for at least one founder. Account opening is often slower than Singapore for non-US-resident founders.",
                 "<strong>The hidden cost of Delaware-without-US-presence:</strong> You'll need a registered agent ($100-$300/year), an EIN, possibly an ITIN for the founder, a US address (registered agent address typically suffices), state and federal tax filings, and 1099 obligations if you pay US contractors. None of this is hard, but it adds up.",
                 "<strong>If your team is in Asia, your customers are in Asia, and you don't yet have US-VC commitments:</strong> Banking through a Singapore Pte Ltd is dramatically simpler.",
             ]),
            ("When Singapore is unambiguously right",
             [
                 "<ul><li><strong>Bootstrapped or angel-funded businesses:</strong> No VC pressure to be Delaware. Tax savings compound. Banking is easier.</li><li><strong>Indian, Vietnamese, Indonesian, MENA founders raising from regional VCs:</strong> Pte Ltd is the regional VC norm. <a href=\"/blog/singapore-flip-structure-indian-startups\">Indian flip structures</a> use Singapore as the holding tier specifically because regional VCs accept it.</li><li><strong>SaaS/services/professional services with non-US revenue base:</strong> Singapore tax efficiency matters more than VC compatibility.</li><li><strong>Family office, holding, IP, treasury vehicles:</strong> Singapore's ~100-DTA network beats Delaware's. <a href=\"/blog/singapore-holding-company-foreign-subsidiaries\">Holding company structuring</a>.</li><li><strong>Asian fintechs, payments, crypto businesses:</strong> MAS regulatory clarity attracts capital that wouldn't touch Delaware-only structures.</li></ul>",
             ]),
            ("When Delaware is unambiguously right",
             [
                 "<ul><li><strong>YC / Techstars / 500 Global accepted:</strong> They write into Delaware C-Corps. Don't fight it.</li><li><strong>You have signed term sheets from US VCs:</strong> They will require Delaware. Just flip or incorporate fresh.</li><li><strong>You'll have material US-resident employees and want clean ESOP:</strong> Delaware avoids cross-border issues.</li><li><strong>Your TAM is overwhelmingly US enterprise/consumer:</strong> Selling to US Fortune 500 from a Delaware vehicle is operationally simpler.</li><li><strong>You plan a US IPO within 5 years:</strong> Save the flip cost; start in Delaware.</li><li><strong>You're a US founder/resident:</strong> CFC and PFIC rules make a foreign opco painful. Default to Delaware unless there's a tax strategy reason not to.</li></ul>",
             ]),
            ("The flip: cost, timeline, and tax",
             [
                 "If you start in Singapore and later need to flip to Delaware (typical reason: US Series A round), here's what's involved:",
                 "<strong>Mechanics.</strong> A new Delaware C-Corp is incorporated as the new top-co. Singapore Pte Ltd shareholders contribute their Pte Ltd shares to the Delaware C-Corp in exchange for Delaware C-Corp shares (a 'share swap' or 'reverse merger' depending on structure). The Singapore Pte Ltd becomes a wholly-owned subsidiary of the Delaware C-Corp.",
                 "<strong>Costs.</strong>",
                 "<ul><li>Legal fees (Singapore + US counsel): $25,000-$50,000 typical</li><li>Tax advice: $5,000-$15,000</li><li>409A valuation post-flip: $1,000-$5,000</li><li>Setup of Delaware C-Corp: $1,000-$3,000 incl. agent and EIN</li><li><strong>Total: ~$30K-$70K</strong></li></ul>",
                 "<strong>Tax exposure.</strong> The contribution may trigger gain recognition for shareholders depending on jurisdiction:",
                 "<ul><li><strong>Singapore-resident shareholders:</strong> Generally no Singapore capital gains tax (Singapore doesn't tax capital gains for individuals). Clean.</li><li><strong>Indian-resident shareholders:</strong> Indian capital gains tax may apply on the contribution. Plan with tax advisors.</li><li><strong>US-resident shareholders:</strong> Section 351 of the Internal Revenue Code may permit a tax-free share swap if structured correctly. Get specialist US tax counsel.</li></ul>",
                 "<strong>Timeline.</strong> 6-10 weeks for a clean flip. Longer if there's existing investor consent required, complex cap table, or cross-border tax planning.",
             ]),
            ("How Karman handles this",
             [
                 'We incorporate Singapore Pte Ltds and run the ongoing services (nominee director, accounting, GST, secretary). For founders evaluating this decision, we recommend our <a href="/tools/business-structure-recommender">structure recommender</a> as a starting point.',
                 "We don't form Delaware C-Corps directly, but we partner with US counsel for flips and dual-structure setups. If you start with us as a Singapore Pte Ltd and later need to flip, we coordinate with US counsel to keep the Singapore side clean (final accounts, IRAS clearance, tax-resident certificate to support DTA claims if relevant).",
            ]),
        ],
        "faqs": [
            ("If I'm based in Singapore, can I just incorporate Delaware and operate from here?",
             "Technically yes, practically painful. You'd be running a US C-Corp from outside the US, which means: 1) you may create a Singapore permanent establishment risk for the Delaware company; 2) you still pay US federal corporate tax at 21%; 3) you have US tax filing obligations even with no US revenue; 4) banking and operations require US presence to function smoothly. Most founders in this situation either incorporate in Singapore, or relocate to the US."),
            ("Is the Delaware C-Corp ESOP really better than Singapore?",
             "For US-resident employees, yes - ISO/NSO mechanics under US tax law are mature and employees expect them. For Singapore-resident employees, the Singapore stock option scheme is comparable and benefits from QESS exemption (up to S$1M lifetime). For mixed teams, the cross-border complexity favors aligning the corporate jurisdiction with the majority of your team."),
            ("Will my Singapore Pte Ltd block me from getting into Y Combinator?",
             "YC accepts founders regardless of starting jurisdiction, but they will require you to flip into a Delaware C-Corp before they invest the standard $500K. Many founders flip during or shortly after the batch. The flip cost (~$30K-$50K) is typically funded from the YC investment itself."),
            ("Do US VCs ever invest into Singapore Pte Ltds without requiring a flip?",
             "Rarely at the seed stage. Some growth-stage funds invest into Singapore VCCs (which are structurally closer to US LP-friendly vehicles). Most US venture capital below growth stage requires Delaware. Asian and ASEAN VCs invest comfortably into Pte Ltds and that's why most regional fundraises start there."),
            ("Can I have a Singapore Pte Ltd own a Delaware C-Corp subsidiary instead of flipping?",
             "Yes, this is a common 'sandwich' structure: Singapore Pte Ltd holdco owns a Delaware C-Corp opco that runs US operations. It works well for businesses with material US revenue but founders/team based outside the US. The structure preserves Singapore tax efficiency at the holdco level while giving US customers a Delaware counterparty. Cross-border tax planning is essential to avoid PFIC/CFC issues."),
        ],
        "sources": [
            ("https://www.iras.gov.sg/taxes/corporate-income-tax/basics-of-corporate-income-tax/corporate-income-tax-rate-rebates-tax-exemption-schemes",
             "IRAS - Corporate Income Tax Rates"),
            ("https://www.irs.gov/businesses/small-businesses-self-employed/corporations",
             "US IRS - Corporations"),
            ("https://corp.delaware.gov/", "Delaware Division of Corporations"),
            ("https://www.iras.gov.sg/taxes/individual-income-tax/employees/income-from-employment/employee-stock-option-(esop)-and-other-forms-of-employee-share-ownership-(esow)",
             "IRAS - Employee Stock Options"),
        ],
        "related": [
            ("singapore-vs-hong-kong-2026", "Comparison", "guide", "Singapore vs Hong Kong 2026",
             "Tax, banking, talent, political risk, and the post-NSL reality.", "12 min read"),
            ("singapore-flip-structure-indian-startups", "Indian Founders", "guide",
             "Singapore Flip Structure for Indian Startups",
             "How to flip your Indian startup to a Singapore holding company. FEMA, ODI, LRS, POEM.", "11 min read"),
            ("ai-startups-incorporating-singapore-2026", "Industry", "guide",
             "AI Startups Incorporating in Singapore (2026)",
             "Why AI founders pick Singapore Pte Ltd, with structure and tax angles.", "10 min read"),
        ],
    },

    # ------------------------------------------------------------------
    # 3. Singapore VCC vs Mauritius GBC for India funds
    # ------------------------------------------------------------------
    {
        "slug": "singapore-vcc-vs-mauritius-gbc-india-funds",
        "title": "Singapore VCC vs Mauritius GBC: Which India Fund Vehicle Wins in 2026?",
        "description": "Mauritius GBC is fading; Singapore VCC is becoming the default India-focused fund vehicle. Tax, treaty, substance, costs, and the post-2024 GAAR/PPT reality.",
        "keyword": "singapore vcc vs mauritius gbc india",
        "tag": "Funds",
        "tag_class": "guide",
        "breadcrumb_short": "VCC vs Mauritius GBC",
        "read_min": 13,
        "lede": "<strong>For new India-focused funds in 2026, Singapore VCC is the default; Mauritius GBC is essentially a legacy structure being wound down.</strong> The combination of India's 2017 LTCG amendment removing the Mauritius treaty advantage, OECD Pillar Two, GAAR/PPT scrutiny, and the explosion of Singapore VCC adoption (over 1,200 VCCs by end-2025) has decisively shifted regional fund structuring. This piece explains why, what each vehicle does, the actual setup and operating costs, and the narrow situations where Mauritius might still apply.",
        "intro_p2": "We cover treaty position, MAS vs FSC supervision, fund administrator availability, costs at three AUM tiers, and the practical conversion path from a legacy Mauritius structure to a Singapore VCC.",
        "sections": [
            ("Headline comparison",
             [
                 '<div class="table-wrap"><table><thead><tr><th>Factor</th><th>Singapore VCC</th><th>Mauritius GBC</th></tr></thead><tbody>'
                 '<tr><td>Year introduced</td><td>2020</td><td>1992 (GBC1, restructured into GBC in 2019)</td></tr>'
                 '<tr><td>Headline tax rate</td><td>17% (with 13O/13U exemption common)</td><td>15% (with partial credit, effective ~3%)</td></tr>'
                 '<tr><td>India LTCG treaty position</td><td>0% on shares acquired after April 2017 (post-amendment) - mostly equivalent</td><td>0% only on shares acquired before 1 April 2017; 7.5%/10%/15% on later acquisitions</td></tr>'
                 '<tr><td>India treaty status (PPT/GAAR risk)</td><td>Lower - Singapore has stronger substance economy</td><td>Higher - PPT challenges have increased post-2017</td></tr>'
                 '<tr><td>Pillar Two (15% global minimum)</td><td>Singapore has implemented domestic top-up</td><td>Mauritius is implementing; effective rates to converge near 15%</td></tr>'
                 '<tr><td>Fund administrator depth</td><td>Wide (Apex, Citco, IQ-EQ, SS&C, Mainstream, Hines, MUFG)</td><td>Narrower (IQ-EQ, Apex, Sanne)</td></tr>'
                 '<tr><td>MAS vs FSC supervision</td><td>MAS - tier 1 globally, well-respected</td><td>FSC - improving but smaller scale</td></tr>'
                 '<tr><td>Substance requirements</td><td>Real Singapore presence required for tax incentives (13O/13U)</td><td>Substance requirements via FSC; meaningful but lighter</td></tr>'
                 '<tr><td>Setup cost (umbrella + 1 sub-fund)</td><td>S$25K-S$80K incl. legal, MAS-related, fund admin onboarding</td><td>$15K-$40K</td></tr>'
                 '<tr><td>Annual operating cost (tier 1)</td><td>S$80K-S$250K depending on AUM and complexity</td><td>$50K-$150K</td></tr>'
                 '<tr><td>LP comfort (LPs evaluating new fund)</td><td>High - become preferred destination 2022-2026</td><td>Mixed - reputational headwinds</td></tr>'
                 '<tr><td>Use cases</td><td>India PE/VC, regional ASEAN, family office, fund-of-funds</td><td>Predominantly India equity (legacy)</td></tr>'
                 '</tbody></table></div>',
             ]),
            ("The 2017 amendment that broke Mauritius",
             [
                 "Mauritius GBC's historical advantage was a single line in the India-Mauritius DTA: capital gains were taxable only in the resident country (Mauritius), and Mauritius didn't tax capital gains. So an Indian portfolio company sold by a Mauritius fund vehicle paid effectively zero tax on the gain.",
                 "<strong>The 2016 protocol, effective from 1 April 2017, ended this.</strong>",
                 "<ul><li>Shares acquired before 1 April 2017: grandfathered. Old rules apply - effectively 0% on capital gains.</li><li>Shares acquired between 1 April 2017 and 31 March 2019: subject to a 50% rate during transition (so ~7.5%-10% effective).</li><li>Shares acquired on or after 1 April 2019: full Indian capital gains tax applies (15-20% LTCG, 30%+ on STCG).</li></ul>",
                 "<strong>India-Singapore DTA was protocol-amended at the same time</strong> (Singapore's protocol effective 1 April 2017) to mirror these rules. This was the moment Singapore and Mauritius effectively reached parity on India tax treatment - and Singapore had every other advantage.",
                 "<strong>Post-2017 dynamic.</strong> A Singapore VCC and a Mauritius GBC investing in Indian shares acquired today face essentially the same Indian tax treatment. The differentiator becomes everything else: substance, regulator, fund administrator depth, LP comfort, banking, and treaty defensibility.",
             ]),
            ("PPT and GAAR: why the Mauritius treaty position is fragile",
             [
                 "Even where the Mauritius treaty technically applies, two anti-abuse rules can still strip the benefit:",
                 "<ol><li><strong>India's General Anti-Avoidance Rule (GAAR), in force since April 2017:</strong> The Indian tax authority can deny treaty benefits if the principal purpose of the arrangement is to obtain a tax benefit, AND the arrangement lacks commercial substance.</li><li><strong>The Multilateral Instrument (MLI) Principal Purpose Test (PPT):</strong> Most modern DTAs - including India-Mauritius post-2019 and India-Singapore - now have a PPT. The test denies treaty benefits if it is reasonable to conclude that obtaining the benefit was one of the principal purposes of the arrangement.</li></ol>",
                 "<strong>What this means in practice:</strong>",
                 "<ul><li>A Mauritius GBC with thin substance (no real fund manager, no real decisions taken in Mauritius, board meetings nominal) is much more vulnerable to GAAR/PPT challenge than a Singapore VCC with a properly resourced Singapore manager</li><li>Indian tax authorities have publicly increased scrutiny of Mauritius structures since 2020. Several high-profile cases have applied PPT to deny capital gains exemption</li><li>Singapore's treaty defence is structurally stronger because Singapore is a real fund management hub - the substance argument is easier to make</li></ul>",
                 "<strong>If you're starting a new fund, defensibility matters more than headline rate.</strong> Singapore wins on defensibility.",
             ]),
            ("What is a Singapore VCC, exactly?",
             [
                 'The Variable Capital Company (VCC) is a Singapore corporate fund vehicle introduced in January 2020. Read our <a href="/glossary/vcc">glossary entry</a> for the full structural breakdown.',
                 "<strong>Key features:</strong>",
                 "<ul><li>Single legal entity that can hold multiple sub-funds with ring-fenced assets and liabilities (umbrella-and-sub-fund structure)</li><li>Variable share capital - capital can be issued and redeemed without the traditional reduction-of-capital procedure (matches LP subscription/redemption mechanics)</li><li>Tax-resident corporate vehicle eligible for Singapore tax incentive schemes (13O - Onshore Fund Tax Exemption, 13U - Enhanced Tier Fund Scheme)</li><li>Regulated by both ACRA (corporate registry) and MAS (substance and AML)</li><li>Can be used for open-ended or closed-ended funds</li></ul>",
                 "<strong>Tax treatment.</strong> A VCC is a Singapore tax resident. Without an incentive scheme, it pays 17% CIT. Most professionally-managed VCCs apply for and receive Section 13O (for funds managed in Singapore with smaller scale) or Section 13U (for funds with at least S$50M committed capital and a substantial Singapore manager) - both of which result in a near-zero effective rate on qualifying income.",
                 "<strong>Substance requirements:</strong>",
                 "<ul><li>13O: Manager must be Singapore-resident, employ at least 2 investment professionals, and pay at least S$200K of business spend in Singapore annually</li><li>13U: Manager must employ at least 3 investment professionals (one earning &gt;S$3,500/month base), incur at least S$200K business spend, and the fund must have at least S$50M committed capital</li></ul>",
                 "These substance bars are real. They're also the reason Singapore VCCs survive PPT scrutiny in a way Mauritius shells don't.",
             ]),
            ("What is a Mauritius GBC, exactly?",
             [
                 "Mauritius's Global Business Company (GBC) is the FSC-licensed company structure used for foreign-source business and investment. Restructured in 2019 (GBC1 was abolished and replaced with the unified GBC), it's the standard Mauritius vehicle for cross-border investment.",
                 "<strong>Key features:</strong>",
                 "<ul><li>Mauritius tax-resident company licensed by the Financial Services Commission (FSC)</li><li>15% headline corporate tax with an 80% partial exemption regime on qualifying foreign-source income, giving an effective rate of ~3%</li><li>Substance requirements via FSC: minimum local employees, local annual expenditure thresholds, and core income-generating activities to be conducted in Mauritius</li><li>Used to access India treaty (now degraded), Africa treaties (still useful), and as a holding vehicle for African investments</li></ul>",
                 "<strong>What Mauritius is still good for:</strong>",
                 "<ul><li>African investments - Mauritius has solid treaty network across sub-Saharan Africa, often better than Singapore</li><li>Existing structures with grandfathered pre-2017 Indian holdings</li><li>Family office structures with African real estate or operating businesses</li></ul>",
                 "<strong>What Mauritius is no longer good for (mostly):</strong>",
                 "<ul><li>New India equity funds - Singapore VCC is the answer</li><li>India-focused PE/VC funds raising new capital - LPs increasingly require Singapore</li></ul>",
             ]),
            ("Cost comparison at three AUM tiers",
             [
                 '<div class="table-wrap"><table><thead><tr><th>AUM tier</th><th>Singapore VCC (annual)</th><th>Mauritius GBC (annual)</th></tr></thead><tbody>'
                 '<tr><td>Sub-S$50M (13O scheme)</td><td>S$80K-S$150K all-in (admin, audit, manager spend, MAS fees)</td><td>$50K-$80K</td></tr>'
                 '<tr><td>S$50M-S$300M (13U scheme)</td><td>S$200K-S$400K all-in</td><td>$80K-$200K</td></tr>'
                 '<tr><td>S$300M+ (13U scheme)</td><td>S$400K+ depending on complexity</td><td>$200K+</td></tr>'
                 '</tbody></table></div>',
                 "<strong>Singapore VCC is more expensive.</strong> The substance requirements (13O minimum S$200K business spend, real fund managers, real audit) drive the cost. This is by design - Singapore is paying for legitimacy.",
                 "<strong>For most funds the LP-attractiveness premium more than offsets the cost.</strong> A fund that closes faster because it's domiciled in Singapore vs Mauritius typically saves more in fundraising time than the incremental annual cost.",
             ]),
            ("LP perspective: what fund LPs are saying",
             [
                 "We work with several VCC fund managers. Common feedback from their LP conversations:",
                 "<ul><li><strong>Tier 1 institutional LPs (sovereign wealth, large pension funds):</strong> Strong preference for Singapore VCC over Mauritius for new commitments. Mauritius mandates often require special board approval. PPT and reputational risks are explicit factors.</li><li><strong>Family offices:</strong> Generally agnostic but trending toward Singapore for new structures. Singapore's MAS regulation gives family office GPs comfort.</li><li><strong>Fund-of-funds:</strong> Increasingly require Singapore as a precondition for investing in India-focused funds.</li><li><strong>Indian HNIs through GIFT City:</strong> Singapore is the natural complement; GIFT City + Singapore VCC is a common structure.</li></ul>",
                 "<strong>Implication:</strong> If you're forming a new India-focused fund and have flexibility, Singapore VCC will close faster, with broader LP base, and survive due diligence questions more cleanly.",
             ]),
            ("Migrating from Mauritius GBC to Singapore VCC",
             [
                 "Singapore allows inward redomiciliation of a foreign company under specific conditions. A Mauritius GBC can theoretically redomicile as a Singapore VCC, but the practical path most managers take is different:",
                 "<strong>Option 1: New VCC for new vintage.</strong> Keep the Mauritius GBC for existing portfolio (often grandfathered or close to wind-down). Form a new Singapore VCC for the new fund vintage. Most common approach.",
                 "<strong>Option 2: Asset transfer.</strong> Establish Singapore VCC, transfer assets from Mauritius GBC to Singapore VCC at fair market value. Tax leakage depends on portfolio composition and LP residency. Used when Mauritius GBC has materially impaired value or wants a clean reset.",
                 "<strong>Option 3: Inward redomiciliation.</strong> Mauritius GBC redomiciles as a Singapore VCC, preserving entity, contracts, and tax history. Requires Singapore to accept (most major jurisdictions can redomicile under Singapore's rules); Mauritius FSC must consent to deregistration. Process is 4-6 months and legally cleaner than asset transfer for established structures.",
                 "<strong>Practical consideration:</strong> Most managers keep their Mauritius vehicle for legacy assets and run new vintages out of Singapore. Migration is rarely worth the operational disruption unless there's a specific reason.",
             ]),
            ("When Mauritius GBC still wins",
             [
                 "The narrow situations where Mauritius is still the right answer:",
                 "<ul><li><strong>Africa-focused funds:</strong> Mauritius's African DTA network is genuinely better than Singapore's. Mauritius-Mozambique, Mauritius-Tunisia, Mauritius-Rwanda, etc. all have stronger withholding tax positions than Singapore equivalents (where they exist at all).</li><li><strong>Existing Mauritius structures with grandfathered Indian holdings:</strong> Don't migrate; the grandfathered shares retain favourable treatment. Run them down or hold to liquidity event.</li><li><strong>Family office private wealth structures with African assets:</strong> Mauritius substance is meaningful, costs are lower, and the regulatory regime is mature.</li><li><strong>Cost-sensitive small private funds (sub-$30M) where 13O substance is uneconomic:</strong> Mauritius can be S$80K-S$150K cheaper annually. For very small funds, this matters.</li></ul>",
                 "Outside these, Singapore VCC is the answer for new India-focused or pan-Asian fund formations.",
             ]),
            ("How Karman handles VCC formation",
             [
                 'We incorporate VCCs (umbrella + sub-funds), set up the manager entity (Singapore Pte Ltd), prepare the 13O/13U application package, source the resident director, coordinate with the fund administrator, and run ongoing corporate secretarial. Read our <a href="/services/vcc-fund-administration">VCC service page</a> for the full scope.',
                 'For India-focused fund managers specifically, our <a href="/for/fintech">fintech industry guide</a> covers the regulatory perimeter (CMS license vs RFMC vs LFMC), and our <a href="/blog/india-vs-singapore-tax-founders">India-Singapore tax piece</a> covers personal tax considerations for the GP.',
            ]),
        ],
        "faqs": [
            ("Is Mauritius GBC dead for new India funds?",
             "Practically yes for most new India-focused funds. The 2017 protocol removed the headline tax advantage, GAAR/PPT increased the defensibility risk, and Singapore VCC adoption created a deeper LP-acceptable alternative. New India fund formations in 2024-2026 we've seen are overwhelmingly Singapore VCC. Mauritius continues to make sense for African investments and grandfathered holdings."),
            ("What's the minimum AUM for a Singapore VCC to be economic?",
             "The 13O scheme has no AUM minimum, but the substance cost (real Singapore manager, S$200K+ business spend, audit, fund administrator) means VCCs below ~S$30M committed capital often struggle to be economic. For sub-S$30M funds, simpler structures (Singapore Pte Ltd as fund or limited partnership) may be more cost-effective. Our <a href=\"/services/vcc-fund-administration\">VCC team</a> helps fund GPs work through this analysis."),
            ("Does a Singapore VCC pay tax on Indian capital gains?",
             "Under the India-Singapore DTA (post-2017 protocol), Indian capital gains on shares acquired before 1 April 2017 are exempt from Indian tax. Shares acquired after that date face Indian capital gains tax (15-20% LTCG, 30%+ STCG). At the Singapore VCC level, qualifying funds under Section 13O or 13U receive substantial Singapore tax exemption on most income types. The combined effective rate depends on portfolio composition and timing of acquisitions."),
            ("Will OECD Pillar Two affect my Singapore VCC?",
             "Pillar Two applies to multinational enterprise groups with consolidated revenue over EUR 750M. Most fund vehicles fall below this threshold. For very large funds (multi-billion AUM with portfolio companies that consolidate), Pillar Two analysis is relevant. Singapore has implemented its domestic top-up tax to align with Pillar Two; this preserves Singapore's primary taxing right. Read our <a href=\"/blog/oecd-pillar-two-singapore-holding-company\">Pillar Two piece</a> for the full mechanics."),
            ("Can a Mauritius GBC have Singapore as the manager jurisdiction?",
             "Technically yes - the manager and the fund vehicle don't have to be in the same jurisdiction. Some legacy structures have Singapore-based fund managers managing Mauritius GBC vehicles. However, this creates Singapore PE risk for the GBC and substance question marks at the GBC level. Most managers in this position eventually move the fund vehicle to Singapore VCC to align manager and vehicle."),
        ],
        "sources": [
            ("https://www.mas.gov.sg/development/variable-capital-companies",
             "MAS - Variable Capital Companies"),
            ("https://www.iras.gov.sg/schemes/disbursement-schemes/variable-capital-companies",
             "IRAS - VCC Tax Schemes (13O / 13U)"),
            ("https://www.fscmauritius.org/", "Mauritius Financial Services Commission"),
            ("https://incometaxindia.gov.in/Pages/international-taxation/dtaa.aspx",
             "Indian Income Tax Department - DTAA"),
        ],
        "related": [
            ("singapore-vs-hong-kong-2026", "Comparison", "guide", "Singapore vs Hong Kong 2026",
             "Tax, banking, talent, political risk, and the post-NSL reality.", "12 min read"),
            ("singapore-vs-delaware-c-corp-2026", "Comparison", "guide",
             "Singapore Pte Ltd vs Delaware C-Corp",
             "Tax, ESOP, fundraising, banking, and what VCs actually accept.", "12 min read"),
            ("oecd-pillar-two-singapore-holding-company", "Tax", "tax",
             "OECD Pillar Two and Your Singapore Holding Company",
             "What the 15% global minimum tax means for Singapore-structured groups.", "9 min read"),
        ],
    },
]


# ============================================================================
# RENDERING (matches priority blogs generator)
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
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-DVKN5K8KSD"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', 'G-DVKN5K8KSD');
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
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Sora:wght@400;600;700;800&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="../../styles.css" />
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
    print(f"\nGenerated {len(BLOGS)} comparison blog posts.")


if __name__ == "__main__":
    main()
