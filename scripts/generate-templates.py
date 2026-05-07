#!/usr/bin/env python3
"""
Generate Karman templates library pages from templates/_templates.json.
Run: python3 scripts/generate-templates.py
"""
import json
import os
import html as htmlmod

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(ROOT, "templates", "_templates.json")
OUT_DIR = os.path.join(ROOT, "templates")
FILES_DIR = os.path.join(ROOT, "templates", "_files")

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
          <div class="footer-col"><h4>Free Resources</h4><ul><li><a href="/tools/">Free Tools</a></li><li><a href="/templates/">Templates</a></li><li><a href="/glossary/">Glossary</a></li><li><a href="/for">Industry Guides</a></li><li><a href="/blog">Blog</a></li></ul></div>
          <div class="footer-col"><h4>Company</h4><ul><li><a href="/#about">About</a></li><li><a href="/#contact">Contact</a></li></ul></div>
        </div>
      </div>
      <div class="footer__bottom"><p>© 2026 Karman Corporate Services Pte Ltd. UEN: 202012889R. 60 Paya Lebar Road, #06-28, Paya Lebar Square, Singapore 409051.</p></div>
    </div>
  </footer>
"""

# Glossary term titles for cross-link labels
TERM_LABELS = {
    "uen": "UEN", "acra": "ACRA", "iras": "IRAS", "bizfile": "BizFile+",
    "ssic-code": "SSIC Code", "agm": "AGM", "egm": "EGM", "fye": "Financial Year End",
    "annual-return": "Annual Return", "eci": "ECI", "form-c-s": "Form C-S",
    "corporate-tax": "Corporate Tax", "gst": "GST", "pte-ltd": "Pte Ltd",
    "sole-proprietorship": "Sole Proprietorship", "llp": "LLP", "vcc": "VCC",
    "section-13o": "Section 13O", "section-13u": "Section 13U", "family-office": "Family Office",
    "ep": "Employment Pass", "s-pass": "S Pass", "tech-pass": "Tech.Pass",
    "one-pass": "ONE Pass", "pep": "Permanent Establishment", "nominee-director": "Nominee Director",
    "corporate-secretary": "Corporate Secretary", "registered-address": "Registered Address",
    "share-capital": "Share Capital", "kyc": "KYC", "beneficial-owner": "Beneficial Owner",
}

# Tool cross-links per template — uses relatedTools list
TEMPLATE_RELATED_TOOLS = {
    "board-resolution": ["business-structure-recommender", "document-checklist"],
    "agm-minutes": ["document-checklist", "incorporation-timeline"],
    "share-transfer": ["cost-calculator", "ssic-code-search"],
    "share-allotment": ["business-structure-recommender", "cost-calculator"],
    "founders-agreement": ["business-structure-recommender", "eligibility-checker"],
    "employment-contract": ["eligibility-checker", "ssic-code-search"],
    "mutual-nda": ["business-structure-recommender", "document-checklist"],
    "ep-cover-letter": ["eligibility-checker", "ssic-code-search"],
}

TOOL_META = {
    "business-structure-recommender": ("Structure Recommender", "Pick the right entity type for your situation."),
    "cost-calculator": ("Cost Calculator", "Estimate your annual corporate services fees."),
    "eligibility-checker": ("Eligibility Checker", "Check if you qualify to incorporate in Singapore."),
    "document-checklist": ("Document Checklist", "All the documents you need for ACRA registration."),
    "incorporation-timeline": ("Incorporation Timeline", "Plan each step from name reservation to bank account."),
    "ssic-code-search": ("SSIC Code Search", "Find the right SSIC 2020 code for your business activity."),
}

CSS = """    .templates-hero { background:linear-gradient(180deg,#fff 0%,#f7f9fc 100%); padding:60px 0 40px; border-bottom:1px solid var(--gray-200); }
    .templates-hero h1 { font-family:'Sora',sans-serif; font-size:clamp(28px,4vw,40px); margin:8px 0 12px; color:#0A2540; }
    .templates-hero p { color:var(--gray-700); max-width:720px; font-size:17px; line-height:1.6; }
    .templates-hero__stat { display:inline-flex; align-items:center; gap:8px; background:#e8f1f8; color:#0d4567; padding:6px 14px; border-radius:999px; font-size:13px; font-weight:600; margin-top:18px; }
    .templates-section { padding:50px 0; }
    .templates-cat { font-family:'Sora',sans-serif; font-size:24px; font-weight:700; color:#0d4567; margin:32px 0 16px; padding-bottom:8px; border-bottom:2px solid #d3e1ee; }
    .templates-cat:first-child { margin-top:0; }
    .templates-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(320px,1fr)); gap:18px; }
    .template-card { background:#fff; border:1px solid var(--gray-200); border-radius:14px; padding:22px 24px; transition:border-color .15s, transform .15s, box-shadow .15s; text-decoration:none; color:inherit; display:flex; flex-direction:column; gap:12px; }
    .template-card:hover { border-color:#0d4567; transform:translateY(-2px); box-shadow:0 6px 18px rgba(13,69,103,.10); }
    .template-card__icon { width:42px; height:42px; border-radius:10px; background:#e8f1f8; color:#0d4567; display:flex; align-items:center; justify-content:center; }
    .template-card__title { font-family:'Sora',sans-serif; font-size:18px; font-weight:700; color:#0A2540; margin:0; }
    .template-card__def { color:var(--gray-700); font-size:14.5px; line-height:1.55; margin:0; flex:1; }
    .template-card__cta { font-size:13.5px; font-weight:700; color:#0d4567; margin-top:auto; }
    .template-page { padding:60px 0 80px; }
    .template-page__breadcrumb { font-size:13px; color:var(--gray-600); margin-bottom:16px; }
    .template-page__breadcrumb a { color:var(--gray-700); text-decoration:none; }
    .template-page__breadcrumb a:hover { color:#0d4567; text-decoration:underline; }
    .template-page__breadcrumb span { margin:0 6px; color:var(--gray-400); }
    .template-page__category { display:inline-block; font-size:11px; font-weight:600; text-transform:uppercase; letter-spacing:.4px; color:#0d4567; background:#e8f1f8; padding:4px 10px; border-radius:6px; margin-bottom:16px; }
    .template-page h1 { font-family:'Sora',sans-serif; font-size:clamp(30px,4.5vw,42px); margin:0 0 12px; color:#0A2540; line-height:1.18; }
    .template-page__lede { font-size:18px; line-height:1.6; color:var(--gray-700); max-width:760px; margin:0 0 28px; }
    .template-page__layout { display:grid; grid-template-columns:1fr 360px; gap:48px; align-items:start; }
    @media (max-width:920px) { .template-page__layout { grid-template-columns:1fr; } }
    .template-page__body h2 { font-family:'Sora',sans-serif; font-size:22px; color:#0A2540; margin:32px 0 12px; }
    .template-page__body h2:first-child { margin-top:0; }
    .template-page__body p { font-size:16px; line-height:1.75; color:var(--gray-800); margin:0 0 14px; }
    .template-page__body ol, .template-page__body ul { font-size:16px; line-height:1.75; color:var(--gray-800); padding-left:22px; margin:0 0 14px; }
    .template-page__body li { margin-bottom:8px; }
    .template-page__body details { background:#f7f9fc; border:1px solid var(--gray-200); border-radius:10px; padding:14px 18px; margin-bottom:10px; }
    .template-page__body details[open] { border-color:#0d4567; }
    .template-page__body summary { font-weight:600; font-size:15.5px; color:#0A2540; cursor:pointer; list-style:none; }
    .template-page__body summary::-webkit-details-marker { display:none; }
    .template-page__body summary::before { content:"+ "; font-weight:700; color:#0d4567; }
    .template-page__body details[open] summary::before { content:"− "; }
    .template-page__body details > p { margin:10px 0 0; font-size:15px; line-height:1.65; color:var(--gray-700); }
    .template-page__download { position:sticky; top:96px; background:linear-gradient(135deg,#0d4567 0%,#0a3a59 100%); border-radius:16px; padding:28px 26px; color:#fff; box-shadow:0 8px 24px rgba(13,69,103,.18); }
    .template-page__download h3 { font-family:'Sora',sans-serif; font-size:20px; margin:0 0 10px; }
    .template-page__download p { font-size:14.5px; line-height:1.55; opacity:.92; margin:0 0 18px; }
    .template-page__download form { display:flex; flex-direction:column; gap:10px; }
    .template-page__download label { font-size:13px; font-weight:600; opacity:.9; }
    .template-page__download input { padding:12px 14px; border:none; border-radius:8px; font-size:15px; font-family:inherit; background:#fff; color:#0A2540; }
    .template-page__download input:focus { outline:2px solid #fff; outline-offset:0; }
    .template-page__download button { padding:13px 20px; background:#fff; color:#0d4567; border:none; border-radius:8px; font-weight:700; font-size:15px; font-family:inherit; cursor:pointer; transition:transform .15s, background .15s; }
    .template-page__download button:hover { transform:translateY(-1px); background:#f0f7ff; }
    .template-page__download button:disabled { opacity:.65; cursor:wait; }
    .template-page__download .small { font-size:12.5px; opacity:.78; margin:14px 0 0; line-height:1.5; }
    .template-page__success { background:#fff; border:1.5px solid #0d4567; border-radius:14px; padding:24px; color:#0A2540; }
    .template-page__success h3 { font-family:'Sora',sans-serif; font-size:18px; margin:0 0 8px; color:#0A2540; }
    .template-page__success p { font-size:14.5px; line-height:1.55; margin:0 0 14px; color:var(--gray-700); }
    .template-page__success a.dl-btn { display:inline-block; padding:12px 20px; background:#0d4567; color:#fff; border-radius:8px; text-decoration:none; font-weight:700; font-size:14.5px; }
    .template-page__success a.dl-btn:hover { background:#0a3a59; }
    .template-page__error { background:#fff5f5; border:1.5px solid #fca5a5; border-radius:10px; padding:14px; color:#991b1b; font-size:14px; margin-top:10px; }
    .template-page__cta-bottom { margin-top:48px; padding:28px 32px; background:#f0f7ff; border-radius:14px; }
    .template-page__cta-bottom h3 { font-family:'Sora',sans-serif; font-size:20px; color:#0A2540; margin:0 0 8px; }
    .template-page__cta-bottom p { font-size:15px; color:var(--gray-700); margin:0 0 14px; line-height:1.55; }
    .template-page__cta-bottom a { display:inline-block; padding:11px 22px; background:#0d4567; color:#fff; border-radius:8px; text-decoration:none; font-weight:700; font-size:14.5px; }
    .template-page__cta-bottom a:hover { background:#0a3a59; }
    .template-related { margin-top:40px; }
    .template-related h2 { font-family:'Sora',sans-serif; font-size:20px; color:#0A2540; margin:0 0 16px; }
    .template-related__grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(220px,1fr)); gap:12px; }
    .template-related__card { display:block; padding:14px 16px; background:#fff; border:1px solid var(--gray-200); border-radius:10px; text-decoration:none; color:#0A2540; transition:all .15s; }
    .template-related__card:hover { border-color:#0d4567; transform:translateY(-1px); box-shadow:0 4px 12px rgba(13,69,103,.08); }
    .template-related__label { display:inline-block; font-size:11px; font-weight:700; text-transform:uppercase; letter-spacing:.4px; color:#0d4567; margin-bottom:4px; }
    .template-related__title { font-weight:700; font-size:15px; margin:0 0 4px; color:#0A2540; }
    .template-related__desc { font-size:13.5px; line-height:1.5; color:var(--gray-700); margin:0; }
    .answer-box { background:#f0f7ff; border-left:4px solid #0d4567; border-radius:0 10px 10px 0; padding:16px 20px; margin:0 0 24px; }
    .answer-box p { margin:0; font-size:16px; line-height:1.65; color:#0A2540; }
    .answer-box strong { color:#0d4567; }
"""


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
  <meta name="robots" content="index, follow" />
  <link rel="canonical" href="https://karman.com.sg{canonical_path}" />

  <meta property="og:type" content="website" />
  <meta property="og:url" content="https://karman.com.sg{canonical_path}" />
  <meta property="og:title" content="{esc(title)}" />
  <meta property="og:description" content="{esc(description)}" />
  <meta property="og:image" content="https://karman.com.sg/logo.png" />
  <meta name="twitter:card" content="summary_large_image" />

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


def render_hub(data):
    templates = data["templates"]
    cats = data["categories"]
    cat_map = {c["id"]: c["name"] for c in cats}

    # Group by category
    by_cat = {}
    for t in templates:
        by_cat.setdefault(t["category"], []).append(t)

    # JSON-LD
    item_list = [
        {
            "@type": "ListItem",
            "position": i + 1,
            "url": f"https://karman.com.sg/templates/{t['slug']}",
            "name": t["title"],
        }
        for i, t in enumerate(templates)
    ]
    ldjson = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "CollectionPage",
                "name": "Free Singapore Corporate Templates",
                "url": "https://karman.com.sg/templates/",
                "description": f"{len(templates)} free Singapore-compliant corporate templates: board resolutions, AGM minutes, share transfer, founders' agreement, employment contract, NDA, EP cover letter.",
                "publisher": {"@type": "Organization", "name": "Karman Corporate Services", "url": "https://karman.com.sg"},
                "mainEntity": {"@type": "ItemList", "itemListElement": item_list},
                "speakable": {
                    "@type": "SpeakableSpecification",
                    "cssSelector": ["h1", ".templates-hero p", ".template-card__def"]
                },
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://karman.com.sg/"},
                    {"@type": "ListItem", "position": 2, "name": "Templates", "item": "https://karman.com.sg/templates/"},
                ],
            },
        ],
    }

    sections = []
    for cat in cats:
        if cat["id"] not in by_cat:
            continue
        sections.append(f'<h2 class="templates-cat" id="cat-{esc(cat["id"])}">{esc(cat["name"])}</h2>')
        sections.append('<div class="templates-grid">')
        for t in by_cat[cat["id"]]:
            sections.append(
                f'<a class="template-card" href="/templates/{esc(t["slug"])}">'
                f'<div class="template-card__icon"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="9" y1="13" x2="15" y2="13"/><line x1="9" y1="17" x2="15" y2="17"/></svg></div>'
                f'<h3 class="template-card__title">{esc(t["title"])}</h3>'
                f'<p class="template-card__def">{esc(t["shortDef"])}</p>'
                f'<span class="template-card__cta">Get template →</span>'
                f"</a>"
            )
        sections.append("</div>")

    title = "Free Singapore Corporate Templates - Board Resolutions, NDAs & More | Karman"
    description = f"{len(templates)} free Singapore-compliant corporate templates: board resolutions, AGM minutes, share transfer, founders' agreement, employment contract, mutual NDA, and EP cover letter."

    body = f"""
  <section class="templates-hero">
    <div class="container">
      <nav class="template-page__breadcrumb" aria-label="Breadcrumb">
        <a href="/">Home</a><span>›</span>
        <span>Templates</span>
      </nav>
      <span class="templates-hero__stat">📄 {len(templates)} Singapore-compliant templates · Free</span>
      <h1>Free Singapore corporate templates</h1>
      <p>Download Singapore-compliant templates for board resolutions, share transfers, employment contracts, NDAs, and EP applications. Drafted by Karman's corporate secretarial team. Email-gated download — no signup needed.</p>
    </div>
  </section>

  <section class="templates-section">
    <div class="container">
{chr(10).join('      ' + l for l in sections)}
    </div>
  </section>

  <section class="templates-section" style="padding-top:0;">
    <div class="container">
      <div class="template-page__cta-bottom">
        <h3>Need help filing or executing these documents?</h3>
        <p>Karman handles ACRA filings, IRAS stamp duty, and statutory register updates as part of our corporate secretarial service. Most clients stay with us as their full-service corporate secretary.</p>
        <a href="/#contact">Talk to our team →</a>
      </div>
    </div>
  </section>

{FOOTER_HTML}

  <script src="/script.js"></script>
</body>
</html>
"""

    head = page_head(title, description, "/templates/", ldjson)
    return head + body


def render_template_page(t, data):
    cat_map = {c["id"]: c["name"] for c in data["categories"]}
    cat_name = cat_map.get(t["category"], "")

    instructions_html = "\n".join(f"        <li>{esc(i)}</li>" for i in t.get("instructions", []))
    faqs_html = "\n".join(
        f"""        <details>
          <summary>{esc(f["q"])}</summary>
          <p>{esc(f["a"])}</p>
        </details>"""
        for f in t.get("faqs", [])
    )

    title = f"{t['title']} (Free Download) | Karman Singapore"
    description = f"{t['shortDef']} Free Singapore-compliant template, drafted by Karman's corporate secretarial team."

    ldjson = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebPage",
                "url": f"https://karman.com.sg/templates/{t['slug']}",
                "name": t["title"],
                "description": t["shortDef"],
                "inLanguage": "en-SG",
                "isPartOf": {"@type": "WebSite", "name": "Karman Corporate Services", "url": "https://karman.com.sg"},
                "speakable": {
                    "@type": "SpeakableSpecification",
                    "cssSelector": ["h1", ".answer-box", ".template-page__lede", ".template-page__body p"]
                }
            },
            {
                "@type": "HowTo",
                "name": f"How to use the {t['title']}",
                "description": t["useCase"],
                "step": [
                    {"@type": "HowToStep", "position": i + 1, "text": s}
                    for i, s in enumerate(t.get("instructions", []))
                ],
            },
            {
                "@type": "FAQPage",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": f["q"],
                        "acceptedAnswer": {"@type": "Answer", "text": f["a"]},
                    }
                    for f in t.get("faqs", [])
                ],
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://karman.com.sg/"},
                    {"@type": "ListItem", "position": 2, "name": "Templates", "item": "https://karman.com.sg/templates/"},
                    {"@type": "ListItem", "position": 3, "name": t["title"], "item": f"https://karman.com.sg/templates/{t['slug']}"},
                ],
            },
        ],
    }

    # Build "Related resources" cross-link block
    related_cards = []
    for tool_slug in TEMPLATE_RELATED_TOOLS.get(t['slug'], []):
        if tool_slug in TOOL_META:
            tname, tdesc = TOOL_META[tool_slug]
            related_cards.append(
                f'<a class="template-related__card" href="/tools/{tool_slug}">'
                f'<span class="template-related__label">Free Tool</span>'
                f'<p class="template-related__title">{esc(tname)}</p>'
                f'<p class="template-related__desc">{esc(tdesc)}</p>'
                f'</a>'
            )
    for term_slug in t.get("relatedTerms", [])[:4]:
        label = TERM_LABELS.get(term_slug, term_slug.replace("-", " ").title())
        related_cards.append(
            f'<a class="template-related__card" href="/glossary/{term_slug}">'
            f'<span class="template-related__label">Glossary</span>'
            f'<p class="template-related__title">{esc(label)}</p>'
            f'<p class="template-related__desc">Plain-English definition for Singapore founders.</p>'
            f'</a>'
        )

    related_html = ""
    if related_cards:
        related_html = f"""
      <div class="template-related">
        <h2>Related Karman tools and definitions</h2>
        <div class="template-related__grid">
          {''.join(related_cards)}
        </div>
      </div>
"""

    # Direct-answer intro for AEO — first sentence answers "what is this template for"
    direct_answer = f"<strong>What this template is.</strong> {esc(t['shortDef'])}"

    head = page_head(title, description, f"/templates/{t['slug']}", ldjson)

    body = f"""
  <section class="template-page">
    <div class="container">
      <nav class="template-page__breadcrumb" aria-label="Breadcrumb">
        <a href="/">Home</a><span>›</span>
        <a href="/templates/">Templates</a><span>›</span>
        <span>{esc(t['title'])}</span>
      </nav>
      <span class="template-page__category">{esc(cat_name)}</span>
      <h1>{esc(t['title'])}</h1>
      <p class="template-page__lede">{esc(t['shortDef'])}</p>

      <div class="template-page__layout">
        <div class="template-page__body">
          <div class="answer-box"><p>{direct_answer}</p></div>
          <h2>When to use this template</h2>
          <p>{esc(t['useCase'])}</p>

          <h2>How to fill it in</h2>
          <ol>
{instructions_html}
          </ol>

          <h2>Frequently asked questions</h2>
{faqs_html}
        </div>

        <aside>
          <div id="dlBox" class="template-page__download">
            <h3>Download this template</h3>
            <p>Enter your email to get the template (.docx). Edit in Word, Google Docs, or Pages.</p>
            <form id="dlForm" novalidate>
              <label for="dlName">Your name</label>
              <input type="text" id="dlName" name="name" required autocomplete="name" placeholder="Jane Tan" />
              <label for="dlEmail">Work email</label>
              <input type="email" id="dlEmail" name="email" required autocomplete="email" placeholder="you@company.com" />
              <button type="submit" id="dlBtn">Email me the template</button>
            </form>
            <p class="small">By submitting you agree to receive this template by email. We'll occasionally email you Singapore corp services tips. Unsubscribe any time.</p>
            <div id="dlError" style="display:none;" class="template-page__error"></div>
          </div>
          <div id="dlSuccess" style="display:none;" class="template-page__success">
            <h3>✓ Sent! Check your email.</h3>
            <p>We've emailed the template to <span id="dlEmailEcho"></span>. While you wait, you can also download it directly:</p>
            <a class="dl-btn" id="dlDirect" href="/templates/_files/{esc(t['slug'])}.docx" download>Download {esc(t['slug'])}.docx</a>
          </div>
        </aside>
      </div>

{related_html}
      <div class="template-page__cta-bottom">
        <h3>Need a corporate secretary to handle this for you?</h3>
        <p>Karman handles ACRA filings, IRAS stamp duty, statutory register updates, and resolution preparation as part of our corporate secretarial service from S$50/month.</p>
        <a href="/#contact">Talk to our team →</a>
      </div>
    </div>
  </section>

{FOOTER_HTML}

  <script src="/script.js"></script>
  <script>
    (function() {{
      const SLUG = {json.dumps(t['slug'])};
      const $form = document.getElementById('dlForm');
      const $btn = document.getElementById('dlBtn');
      const $err = document.getElementById('dlError');
      const $box = document.getElementById('dlBox');
      const $success = document.getElementById('dlSuccess');
      const $emailEcho = document.getElementById('dlEmailEcho');

      $form.addEventListener('submit', async function(e) {{
        e.preventDefault();
        $err.style.display = 'none';
        const name = document.getElementById('dlName').value.trim();
        const email = document.getElementById('dlEmail').value.trim();
        if (!name || !email) {{
          $err.textContent = 'Please enter your name and email.';
          $err.style.display = 'block';
          return;
        }}
        $btn.disabled = true;
        $btn.textContent = 'Sending...';
        try {{
          const res = await fetch('/api/send-template', {{
            method: 'POST',
            headers: {{ 'Content-Type': 'application/json' }},
            body: JSON.stringify({{ name, email, slug: SLUG }}),
          }});
          if (!res.ok) {{
            const data = await res.json().catch(()=>({{ error: 'Failed to send' }}));
            throw new Error(data.error || 'Failed to send');
          }}
          $emailEcho.textContent = email;
          $box.style.display = 'none';
          $success.style.display = 'block';
        }} catch (err) {{
          $err.textContent = err.message || 'Something went wrong. Please try again.';
          $err.style.display = 'block';
          $btn.disabled = false;
          $btn.textContent = 'Email me the template';
        }}
      }});
    }})();
  </script>
</body>
</html>
"""

    return head + body


def main():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Hub
    hub_path = os.path.join(OUT_DIR, "index.html")
    with open(hub_path, "w", encoding="utf-8") as f:
        f.write(render_hub(data))
    print(f"Wrote {hub_path}")

    # Each template
    for t in data["templates"]:
        slug = t["slug"]
        dest_dir = os.path.join(OUT_DIR, slug)
        os.makedirs(dest_dir, exist_ok=True)
        dest = os.path.join(dest_dir, "index.html")
        with open(dest, "w", encoding="utf-8") as f:
            f.write(render_template_page(t, data))
        print(f"Wrote {dest}")

    print(f"\nDone. {len(data['templates'])} templates + 1 hub.")


if __name__ == "__main__":
    main()
