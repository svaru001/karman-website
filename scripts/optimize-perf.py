#!/usr/bin/env python3
"""Apply Lighthouse performance fixes site-wide.

Three transformations per page:
  1. Defer GTM until requestIdleCallback / window load (saves ~53 KiB on FCP/TBT).
  2. Make Google Fonts CSS non-blocking via media=print swap (saves render-blocking ~780 ms).
  3. Add explicit width/height + fetchpriority=high to the FIRST nav__logo-img on the page
     (fixes CLS + LCP discovery).

Skips files already converted (idempotent).
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

GTM_OLD_RE = re.compile(
    r'  <script async src="https://www\.googletagmanager\.com/gtag/js\?id=G-DVKN5K8KSD"></script>\s*\n'
    r'  <script>\s*\n'
    r'    window\.dataLayer = window\.dataLayer \|\| \[\];\s*\n'
    r'    function gtag\(\)\{dataLayer\.push\(arguments\);\}\s*\n'
    r"    gtag\('js', new Date\(\)\);\s*\n"
    r"    gtag\('config', 'G-DVKN5K8KSD'\);\s*\n"
    r'  </script>'
)

GTM_NEW = """  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'G-DVKN5K8KSD');
    function loadGTM(){
      if (window.__gtmLoaded) return;
      window.__gtmLoaded = true;
      var s = document.createElement('script');
      s.async = true;
      s.src = 'https://www.googletagmanager.com/gtag/js?id=G-DVKN5K8KSD';
      document.head.appendChild(s);
    }
    if ('requestIdleCallback' in window) {
      requestIdleCallback(loadGTM, {timeout: 3000});
    } else {
      window.addEventListener('load', function(){ setTimeout(loadGTM, 1500); });
    }
  </script>"""


# Match a single render-blocking <link ...rel="stylesheet"...> pointing at fonts.googleapis.com/css2.
# Avoids matching links that are already preload, media="print", or inside a <noscript>.
FONT_BLOCKING_RE = re.compile(
    r'  <link href="(https://fonts\.googleapis\.com/css2[^"]+)" rel="stylesheet"\s*/?>'
)


def font_replacement(match):
    url = match.group(1)
    return (
        f'  <link rel="preload" as="style" href="{url}" />\n'
        f'  <link rel="stylesheet" href="{url}" media="print" onload="this.media=\'all\'" />\n'
        f'  <noscript><link rel="stylesheet" href="{url}" /></noscript>'
    )


# Match the FIRST nav__logo-img on the page only. We require it not already have width attr.
LOGO_RE = re.compile(
    r'(<img src="/logo\.svg" alt="Karman" class="nav__logo-img")(>)'
)


def transform(text: str, fname: str) -> tuple[str, dict]:
    changes = {"gtm": False, "fonts": 0, "logo_header": False, "logo_footer": False}

    # --- 1. GTM ---
    if GTM_OLD_RE.search(text):
        text = GTM_OLD_RE.sub(GTM_NEW, text, count=1)
        changes["gtm"] = True

    # --- 2. Fonts ---
    new_text, n = FONT_BLOCKING_RE.subn(font_replacement, text)
    if n > 0:
        text = new_text
        changes["fonts"] = n

    # --- 3. Logo (first occurrence: header => fetchpriority=high; second: footer => loading=lazy) ---
    matches = list(LOGO_RE.finditer(text))
    if matches:
        # Replace last → first so offsets stay valid
        for i, m in enumerate(reversed(matches)):
            idx_from_top = len(matches) - 1 - i
            if idx_from_top == 0:
                replacement = m.group(1) + ' width="124" height="40" fetchpriority="high"' + m.group(2)
                changes["logo_header"] = True
            else:
                replacement = m.group(1) + ' width="124" height="40" loading="lazy"' + m.group(2)
                changes["logo_footer"] = True
            text = text[:m.start()] + replacement + text[m.end():]

    return text, changes


def main():
    files = sorted(p for p in ROOT.rglob("*.html")
                   if "node_modules" not in p.parts and ".git" not in p.parts)
    n_changed = 0
    summary = {"gtm": 0, "fonts": 0, "logo_header": 0, "logo_footer": 0}
    for f in files:
        original = f.read_text(encoding="utf-8")
        new, changes = transform(original, f.name)
        if new != original:
            f.write_text(new, encoding="utf-8")
            n_changed += 1
            for k, v in changes.items():
                if isinstance(v, bool):
                    summary[k] += 1 if v else 0
                else:
                    summary[k] += v
            print(f"  {f.relative_to(ROOT)}: {changes}")
    print(f"\nFiles changed: {n_changed} of {len(files)}")
    print(f"GTM blocks deferred: {summary['gtm']}")
    print(f"Font links made non-blocking: {summary['fonts']}")
    print(f"Header logos with fetchpriority=high: {summary['logo_header']}")
    print(f"Footer logos with loading=lazy: {summary['logo_footer']}")


if __name__ == "__main__":
    main()
