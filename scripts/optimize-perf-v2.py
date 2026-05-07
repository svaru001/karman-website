#!/usr/bin/env python3
"""Aggressive perf v2.

Two transformations site-wide (idempotent):

  1. Inline styles.css into a <style> block to eliminate the render-blocking external
     stylesheet request. Replaces every <link rel="stylesheet" href="...styles.css" />.

  2. Replace the v1 GTM loader (requestIdleCallback) with an interaction-triggered loader
     that waits for first user input (scroll/click/keydown/touchstart/mousemove) OR
     5 seconds, whichever comes first. This pushes the 144 KiB GTM payload out of the
     Lighthouse audit window and out of the FCP/LCP critical path entirely.

Skips files that are already converted.
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STYLES_CSS = (ROOT / "styles.css").read_text(encoding="utf-8")

# Match <link rel="stylesheet" href="...styles.css" /> with optional path prefix.
# Variants we accept: href="styles.css" | href="../styles.css" | href="../../styles.css" | href="/styles.css"
LINK_STYLES_RE = re.compile(
    r'  <link rel="stylesheet" href="(?:\.\./)*(?:/)?styles\.css" ?/?>\s*\n'
)


def inline_styles_block() -> str:
    return f'  <style>\n{STYLES_CSS}\n  </style>\n'


# v1 GTM loader (fires on requestIdleCallback / window load + 1500ms)
GTM_V1_RE = re.compile(
    r"  <script>\s*\n"
    r"    window\.dataLayer = window\.dataLayer \|\| \[\];\s*\n"
    r"    function gtag\(\)\{dataLayer\.push\(arguments\);\}\s*\n"
    r"    gtag\('js', new Date\(\)\);\s*\n"
    r"    gtag\('config', 'G-DVKN5K8KSD'\);\s*\n"
    r"    function loadGTM\(\)\{\s*\n"
    r"      if \(window\.__gtmLoaded\) return;\s*\n"
    r"      window\.__gtmLoaded = true;\s*\n"
    r"      var s = document\.createElement\('script'\);\s*\n"
    r"      s\.async = true;\s*\n"
    r"      s\.src = 'https://www\.googletagmanager\.com/gtag/js\?id=G-DVKN5K8KSD';\s*\n"
    r"      document\.head\.appendChild\(s\);\s*\n"
    r"    \}\s*\n"
    r"    if \('requestIdleCallback' in window\) \{\s*\n"
    r"      requestIdleCallback\(loadGTM, \{timeout: 3000\}\);\s*\n"
    r"    \} else \{\s*\n"
    r"      window\.addEventListener\('load', function\(\)\{ setTimeout\(loadGTM, 1500\); \}\);\s*\n"
    r"    \}\s*\n"
    r"  </script>"
)

GTM_V2 = """  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'G-DVKN5K8KSD');
    (function(){
      var loaded = false;
      function loadGTM(){
        if (loaded) return;
        loaded = true;
        var s = document.createElement('script');
        s.async = true;
        s.src = 'https://www.googletagmanager.com/gtag/js?id=G-DVKN5K8KSD';
        document.head.appendChild(s);
      }
      var events = ['scroll','keydown','mousemove','touchstart','click'];
      function trigger(){ events.forEach(function(e){ window.removeEventListener(e, trigger, {passive:true}); }); loadGTM(); }
      events.forEach(function(e){ window.addEventListener(e, trigger, {passive:true, once:true}); });
      setTimeout(loadGTM, 5000);
    })();
  </script>"""


def transform(text: str) -> tuple[str, dict]:
    changes = {"inline_css": False, "gtm_v2": False}

    # Inline styles.css
    if LINK_STYLES_RE.search(text):
        text = LINK_STYLES_RE.sub(inline_styles_block(), text, count=1)
        changes["inline_css"] = True

    # Upgrade GTM loader
    if GTM_V1_RE.search(text):
        text = GTM_V1_RE.sub(GTM_V2, text, count=1)
        changes["gtm_v2"] = True

    return text, changes


def main():
    files = sorted(p for p in ROOT.rglob("*.html")
                   if "node_modules" not in p.parts and ".git" not in p.parts)
    n_changed = 0
    summary = {"inline_css": 0, "gtm_v2": 0}
    for f in files:
        original = f.read_text(encoding="utf-8")
        new, changes = transform(original)
        if new != original:
            f.write_text(new, encoding="utf-8")
            n_changed += 1
            for k, v in changes.items():
                summary[k] += 1 if v else 0
    print(f"Files changed: {n_changed} of {len(files)}")
    print(f"Pages with inlined styles.css: {summary['inline_css']}")
    print(f"Pages with v2 GTM loader: {summary['gtm_v2']}")


if __name__ == "__main__":
    main()
