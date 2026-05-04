#!/usr/bin/env python3
"""
Generate Karman glossary pages from glossary/_terms.json.
Run: python3 scripts/generate-glossary.py
"""
import json
import os
import sys
import html as htmlmod

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TERMS_FILE = os.path.join(ROOT, "glossary", "_terms.json")
GLOSSARY_DIR = os.path.join(ROOT, "glossary")

NAV_HTML = """  <header class="header" id="header">
    <nav class="nav container" aria-label="Main navigation">
      <a href="/" class="nav__logo"><img src="/logo.svg" alt="Karman" class="nav__logo-img"></a>
      <ul class="nav__menu" id="navMenu">
        <li class="nav__item"><a href="{home_prefix}#services" class="nav__link">Services</a></li>
        <li class="nav__item"><a href="/about" class="nav__link">About</a></li>
        <li class="nav__item"><a href="/tools/" class="nav__link">Free Tools <span class="nav__badge">Free</span></a></li>
        <li class="nav__item"><a href="/blog" class="nav__link">Blog</a></li>
        <li class="nav__item"><a href="{home_prefix}#faq" class="nav__link">FAQ</a></li>
      <div class="nav__actions">
        <a href="{home_prefix}#contact" class="btn btn--secondary">Contact us</a>
        <a href="{home_prefix}#get-started" class="btn btn--primary">Get started</a>
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
          <div class="footer__badges"><span class="badge">ACRA Registered</span><span class="badge">MAS Regulated</span>  <a class="footer__social-link" href="https://www.linkedin.com/company/karman-advisory-singapore/" target="_blank" rel="noopener" aria-label="Karman on LinkedIn"><svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor" xmlns="http://www.w3.org/2000/svg"><path d="M20.45 20.45h-3.55v-5.57c0-1.33-.03-3.04-1.85-3.04-1.85 0-2.14 1.45-2.14 2.94v5.67H9.36V9h3.41v1.56h.05c.48-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.45v6.29zM5.34 7.43a2.06 2.06 0 1 1 0-4.12 2.06 2.06 0 0 1 0 4.12zM7.12 20.45H3.56V9h3.56v11.45zM22.22 0H1.77C.79 0 0 .77 0 1.72v20.56C0 23.23.79 24 1.77 24h20.45c.98 0 1.78-.77 1.78-1.72V1.72C24 .77 23.2 0 22.22 0z"/></svg></a>
          </div>
        </div>
        <div class="footer__links">
          <div class="footer-col"><h4>Services</h4><ul><li><a href="/#incorporation">Company Incorporation</a></li><li><a href="/#secretary">Corporate Secretarial</a></li><li><a href="/#accounting">Accounting</a></li></ul></div>
          <div class="footer-col"><h4>Free Tools</h4><ul><li><a href="/tools/business-structure-recommender">Structure Recommender</a></li><li><a href="/tools/cost-calculator">Cost Calculator</a></li><li><a href="/tools/eligibility-checker">Eligibility Checker</a></li><li><a href="/tools/document-checklist">Document Checklist</a></li><li><a href="/tools/ssic-code-search">SSIC Code Search</a></li><li><a href="/glossary/">Glossary</a></li></ul></div>
          <div class="footer-col"><h4>Company</h4><ul><li><a href="/#about">About</a></li><li><a href="/#contact">Contact</a></li></ul></div>
        </div>
      </div>
      <div class="footer__bottom"><p>© 2026 Karman Corporate Services Pte Ltd. UEN: 202012889R. 60 Paya Lebar Road, #06-28, Paya Lebar Square, Singapore 409051.</p></div>
    </div>
  </footer>
"""

GLOSSARY_CSS = """    .glossary-hero { background:linear-gradient(180deg,#fff 0%,#f7f9fc 100%); padding:60px 0 40px; border-bottom:1px solid var(--gray-200); }
    .glossary-hero h1 { font-family:'Sora',sans-serif; font-size:clamp(28px,4vw,40px); margin:8px 0 12px; color:#0A2540; }
    .glossary-hero p { color:var(--gray-700); max-width:680px; font-size:17px; line-height:1.6; }
    .glossary-search { display:flex; gap:12px; flex-wrap:wrap; margin-top:24px; max-width:680px; }
    .glossary-search__input { flex:1; min-width:240px; padding:14px 16px; border:1.5px solid var(--gray-300); border-radius:10px; font-size:16px; font-family:inherit; background:#fff; }
    .glossary-search__input:focus { outline:none; border-color:#0d4567; box-shadow:0 0 0 3px rgba(13,69,103,.12); }
    .glossary-search__filter { padding:14px 16px; border:1.5px solid var(--gray-300); border-radius:10px; font-size:15px; font-family:inherit; background:#fff; cursor:pointer; min-width:200px; }
    .glossary-section { padding:50px 0; }
    .glossary-letter { font-family:'Sora',sans-serif; font-size:30px; font-weight:700; color:#0d4567; margin:32px 0 16px; padding-bottom:8px; border-bottom:2px solid #d3e1ee; }
    .glossary-letter:first-child { margin-top:0; }
    .glossary-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(300px,1fr)); gap:16px; }
    .glossary-card { background:#fff; border:1px solid var(--gray-200); border-radius:12px; padding:18px 20px; transition:border-color .15s, transform .15s, box-shadow .15s; text-decoration:none; color:inherit; display:block; }
    .glossary-card:hover { border-color:#0d4567; transform:translateY(-2px); box-shadow:0 4px 14px rgba(13,69,103,.08); }
    .glossary-card__title { font-family:'Sora',sans-serif; font-size:18px; font-weight:700; color:#0A2540; margin:0 0 6px; }
    .glossary-card__category { display:inline-block; font-size:11px; font-weight:600; text-transform:uppercase; letter-spacing:.4px; color:#0d4567; background:#e8f1f8; padding:3px 8px; border-radius:6px; margin-bottom:10px; }
    .glossary-card__def { color:var(--gray-700); font-size:14.5px; line-height:1.55; margin:0; }
    .glossary-empty { text-align:center; padding:60px 20px; color:var(--gray-600); }
    .term-page { padding:60px 0; }
    .term-page__breadcrumb { font-size:13px; color:var(--gray-600); margin-bottom:16px; }
    .term-page__breadcrumb a { color:var(--gray-700); text-decoration:none; }
    .term-page__breadcrumb a:hover { color:#0d4567; text-decoration:underline; }
    .term-page__breadcrumb span { margin:0 6px; color:var(--gray-400); }
    .term-page__category { display:inline-block; font-size:11px; font-weight:600; text-transform:uppercase; letter-spacing:.4px; color:#0d4567; background:#e8f1f8; padding:4px 10px; border-radius:6px; margin-bottom:16px; }
    .term-page h1 { font-family:'Sora',sans-serif; font-size:clamp(32px,5vw,46px); margin:0 0 8px; color:#0A2540; line-height:1.15; }
    .term-page__fullname { font-size:18px; color:var(--gray-600); font-weight:500; margin:0 0 24px; }
    .term-page__short { font-size:19px; line-height:1.55; color:#0A2540; font-weight:500; padding:18px 22px; background:#f0f7ff; border-left:4px solid #0d4567; border-radius:0 10px 10px 0; margin:0 0 32px; }
    .term-page__body { font-size:16px; line-height:1.75; color:var(--gray-800); max-width:760px; }
    .term-page__body h2 { font-family:'Sora',sans-serif; font-size:22px; color:#0A2540; margin:36px 0 12px; }
    .term-page__body p { margin:0 0 14px; }
    .term-page__related { margin-top:48px; padding-top:32px; border-top:1px solid var(--gray-200); }
    .term-page__related h2 { font-family:'Sora',sans-serif; font-size:20px; color:#0A2540; margin:0 0 16px; }
    .term-page__related-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(220px,1fr)); gap:12px; }
    .term-page__related a { display:block; padding:12px 16px; background:var(--gray-50); border:1px solid var(--gray-200); border-radius:10px; text-decoration:none; color:#0A2540; font-weight:600; font-size:14.5px; transition:all .15s; }
    .term-page__related a:hover { background:#0d4567; color:#fff; border-color:#0d4567; }
    .term-page__cta { margin-top:40px; padding:24px 28px; background:linear-gradient(135deg,#0d4567 0%,#0a3a59 100%); border-radius:14px; color:#fff; }
    .term-page__cta h3 { font-family:'Sora',sans-serif; font-size:20px; margin:0 0 8px; }
    .term-page__cta p { margin:0 0 16px; opacity:.92; font-size:15px; line-height:1.5; }
    .term-page__cta a { display:inline-block; padding:11px 22px; background:#fff; color:#0d4567; border-radius:8px; text-decoration:none; font-weight:700; font-size:14.5px; }
    .term-page__cta a:hover { background:#f0f7ff; }
"""


def esc(s):
    return htmlmod.escape(s, quote=True) if s else ""


def first_letter(t):
    return t["title"][0].upper()


def get_term(slug, terms_by_slug):
    return terms_by_slug.get(slug)


def render_hub(data):
    terms = sorted(data["terms"], key=lambda t: t["title"].lower())
    cats = data["categories"]
    cat_map = {c["id"]: c["name"] for c in cats}

    # Group by first letter
    groups = {}
    for t in terms:
        groups.setdefault(first_letter(t), []).append(t)

    # JSON-LD: DefinedTermSet
    has_part = [
        {
            "@type": "DefinedTerm",
            "name": t["title"],
            "url": f"https://karman.com.sg/glossary/{t['slug']}",
            "description": t["shortDef"],
        }
        for t in terms
    ]
    ldjson = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "DefinedTermSet",
                "name": "Singapore Business Glossary",
                "url": "https://karman.com.sg/glossary/",
                "description": "Plain-English definitions of Singapore corporate, tax, immigration, and fund-management terms used by founders, fund managers, and family offices.",
                "publisher": {"@type": "Organization", "name": "Karman Corporate Services", "url": "https://karman.com.sg"},
                "hasDefinedTerm": has_part,
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://karman.com.sg/"},
                    {"@type": "ListItem", "position": 2, "name": "Glossary", "item": "https://karman.com.sg/glossary/"},
                ],
            },
        ],
    }

    cards = []
    for letter in sorted(groups.keys()):
        cards.append(f'<h2 class="glossary-letter" id="letter-{letter}">{letter}</h2>')
        cards.append('<div class="glossary-grid">')
        for t in groups[letter]:
            cat_name = cat_map.get(t["category"], "")
            cards.append(
                f'<a class="glossary-card" data-cat="{esc(t["category"])}" data-text="{esc((t["title"]+" "+t["fullName"]+" "+(" ".join(t.get("aliases",[])))).lower())}" href="/glossary/{esc(t["slug"])}">'
                f'<span class="glossary-card__category">{esc(cat_name)}</span>'
                f'<h3 class="glossary-card__title">{esc(t["title"])}</h3>'
                f'<p class="glossary-card__def">{esc(t["shortDef"])}</p>'
                f"</a>"
            )
        cards.append("</div>")

    cat_options = '\n'.join(
        f'            <option value="{esc(c["id"])}">{esc(c["name"])}</option>' for c in cats
    )

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
  <title>Singapore Business Glossary - ACRA, IRAS, EP, VCC Terms Explained | Karman</title>
  <meta name="description" content="Plain-English glossary of Singapore corporate, tax, immigration, and VCC fund terms. {len(terms)} definitions for founders, fund managers, and family offices." />
  <meta name="robots" content="index, follow" />
  <link rel="canonical" href="https://karman.com.sg/glossary/" />

  <meta property="og:type" content="website" />
  <meta property="og:url" content="https://karman.com.sg/glossary/" />
  <meta property="og:title" content="Singapore Business Glossary - ACRA, IRAS, EP, VCC Terms Explained | Karman" />
  <meta property="og:description" content="Plain-English glossary of Singapore corporate, tax, immigration, and VCC fund terms." />
  <meta property="og:image" content="https://karman.com.sg/logo.png" />
  <meta name="twitter:card" content="summary_large_image" />

  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Sora:wght@400;600;700;800&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="/styles.css" />

  <script type="application/ld+json">
{json.dumps(ldjson, ensure_ascii=False, indent=2)}
  </script>

  <style>
{GLOSSARY_CSS}  </style>
</head>
<body>

{NAV_HTML.format(home_prefix="/")}

  <section class="glossary-hero">
    <div class="container">
      <nav class="term-page__breadcrumb" aria-label="Breadcrumb">
        <a href="/">Home</a><span>›</span>
        <span>Glossary</span>
      </nav>
      <h1>Singapore business glossary</h1>
      <p>Plain-English definitions of every Singapore corporate, tax, immigration, and VCC fund term you'll meet during incorporation, compliance, and growth. Updated for 2026.</p>
      <div class="glossary-search">
        <input type="text" id="glossarySearch" class="glossary-search__input" placeholder="Search a term (e.g. UEN, EP, VCC, FYE)" aria-label="Search glossary" />
        <select id="glossaryFilter" class="glossary-search__filter" aria-label="Filter by category">
          <option value="">All categories</option>
{cat_options}
        </select>
      </div>
    </div>
  </section>

  <section class="glossary-section">
    <div class="container">
      <div id="glossaryContent">
{chr(10).join('        ' + l for l in cards)}
      </div>
      <div id="glossaryEmpty" class="glossary-empty" style="display:none;">
        <p>No terms match your search.</p>
        <p style="font-size:14px;">Don't see a term? <a href="/#contact">Tell us</a> and we'll add it.</p>
      </div>
    </div>
  </section>

{FOOTER_HTML}

  <script src="/script.js"></script>
  <script>
    (function() {{
      const $search = document.getElementById('glossarySearch');
      const $filter = document.getElementById('glossaryFilter');
      const $content = document.getElementById('glossaryContent');
      const $empty = document.getElementById('glossaryEmpty');

      function applyFilter() {{
        const q = ($search.value || '').trim().toLowerCase();
        const cat = $filter.value;
        let visibleCount = 0;
        $content.querySelectorAll('.glossary-card').forEach(card => {{
          const text = card.dataset.text || '';
          const c = card.dataset.cat || '';
          const matches = (!q || text.includes(q)) && (!cat || c === cat);
          card.style.display = matches ? '' : 'none';
          if (matches) visibleCount++;
        }});
        $content.querySelectorAll('.glossary-letter').forEach(letter => {{
          const next = letter.nextElementSibling;
          if (!next) return;
          const anyVisible = Array.from(next.querySelectorAll('.glossary-card')).some(c => c.style.display !== 'none');
          letter.style.display = anyVisible ? '' : 'none';
          next.style.display = anyVisible ? '' : 'none';
        }});
        $empty.style.display = visibleCount === 0 ? 'block' : 'none';
      }}

      $search.addEventListener('input', applyFilter);
      $filter.addEventListener('change', applyFilter);
    }})();
  </script>
</body>
</html>
"""


def render_term_page(term, data):
    cat_map = {c["id"]: c["name"] for c in data["categories"]}
    terms_by_slug = {t["slug"]: t for t in data["terms"]}
    cat_name = cat_map.get(term["category"], "")
    related_terms = [get_term(s, terms_by_slug) for s in term.get("related", []) if get_term(s, terms_by_slug)]

    paragraphs = [p.strip() for p in term["definition"].split("\n\n") if p.strip()]
    body_html = "\n".join(f"        <p>{esc(p)}</p>" for p in paragraphs)

    example_html = ""
    if term.get("example"):
        example_html = f'        <h2>Example</h2>\n        <p>{esc(term["example"])}</p>'

    related_html = ""
    if related_terms:
        cards_html = "\n".join(
            f'          <a href="/glossary/{esc(t["slug"])}">{esc(t["title"])} - {esc(t["shortDef"][:80])}{("..." if len(t["shortDef"])>80 else "")}</a>'
            for t in related_terms
        )
        related_html = f"""      <div class="term-page__related">
        <h2>Related terms</h2>
        <div class="term-page__related-grid">
{cards_html}
        </div>
      </div>"""

    extra_links = []
    if term.get("relatedBlog"):
        extra_links.append(f'<a href="{esc(term["relatedBlog"])}">Read the full guide →</a>')
    if term.get("relatedTool"):
        extra_links.append(f'<a href="{esc(term["relatedTool"])}">Try the tool →</a>')
    extra_links_html = ""
    if extra_links:
        extra_links_html = f"""      <div class="term-page__cta">
        <h3>Need help with {esc(term["title"])}?</h3>
        <p>Karman handles incorporation, compliance, and ongoing corporate services for Singapore companies, family offices, and VCCs.</p>
        <a href="/#contact">Talk to our team →</a>
      </div>"""

    ldjson = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "DefinedTerm",
                "name": term["title"],
                "alternateName": [term["fullName"]] + term.get("aliases", []),
                "description": term["shortDef"],
                "url": f"https://karman.com.sg/glossary/{term['slug']}",
                "inDefinedTermSet": {
                    "@type": "DefinedTermSet",
                    "name": "Singapore Business Glossary",
                    "url": "https://karman.com.sg/glossary/",
                },
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://karman.com.sg/"},
                    {"@type": "ListItem", "position": 2, "name": "Glossary", "item": "https://karman.com.sg/glossary/"},
                    {"@type": "ListItem", "position": 3, "name": term["title"], "item": f"https://karman.com.sg/glossary/{term['slug']}"},
                ],
            },
        ],
    }

    page_title = f"{term['title']} ({term['fullName']}) - Singapore Glossary | Karman"
    meta_desc = f"{term['shortDef']} Plain-English definition of {term['title']} for Singapore founders and fund managers."

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
  <title>{esc(page_title)}</title>
  <meta name="description" content="{esc(meta_desc)}" />
  <meta name="robots" content="index, follow" />
  <link rel="canonical" href="https://karman.com.sg/glossary/{esc(term['slug'])}" />

  <meta property="og:type" content="article" />
  <meta property="og:url" content="https://karman.com.sg/glossary/{esc(term['slug'])}" />
  <meta property="og:title" content="{esc(page_title)}" />
  <meta property="og:description" content="{esc(meta_desc)}" />
  <meta property="og:image" content="https://karman.com.sg/logo.png" />
  <meta name="twitter:card" content="summary_large_image" />

  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Sora:wght@400;600;700;800&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="/styles.css" />

  <script type="application/ld+json">
{json.dumps(ldjson, ensure_ascii=False, indent=2)}
  </script>

  <style>
{GLOSSARY_CSS}  </style>
</head>
<body>

{NAV_HTML.format(home_prefix="/")}

  <section class="term-page">
    <div class="container">
      <nav class="term-page__breadcrumb" aria-label="Breadcrumb">
        <a href="/">Home</a><span>›</span>
        <a href="/glossary/">Glossary</a><span>›</span>
        <span>{esc(term['title'])}</span>
      </nav>
      <span class="term-page__category">{esc(cat_name)}</span>
      <h1>{esc(term['title'])}</h1>
      <p class="term-page__fullname">{esc(term['fullName'])}</p>
      <p class="term-page__short">{esc(term['shortDef'])}</p>
      <div class="term-page__body">
        <h2>Definition</h2>
{body_html}
{example_html}
      </div>
{related_html}
{extra_links_html}
    </div>
  </section>

{FOOTER_HTML}

  <script src="/script.js"></script>
</body>
</html>
"""


def main():
    with open(TERMS_FILE) as f:
        data = json.load(f)

    # Hub
    hub_path = os.path.join(GLOSSARY_DIR, "index.html")
    with open(hub_path, "w") as f:
        f.write(render_hub(data))
    print(f"  + {hub_path}")

    # Term pages
    count = 0
    for term in data["terms"]:
        slug = term["slug"]
        d = os.path.join(GLOSSARY_DIR, slug)
        os.makedirs(d, exist_ok=True)
        p = os.path.join(d, "index.html")
        with open(p, "w") as f:
            f.write(render_term_page(term, data))
        count += 1
        print(f"  + {p}")
    print(f"\nGenerated {count} term pages + 1 hub.")


if __name__ == "__main__":
    main()
