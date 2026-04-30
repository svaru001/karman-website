#!/usr/bin/env node
/* Inject LinkedIn social link into footer__brand block of every HTML page.
   Handles both footer variants:
   - Style A: footer__brand has footer__badges (homepage, services)
   - Style B: footer__brand has just logo + <p> (faq, blog posts) */

const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const SENTINEL = 'footer__social';

const SOCIAL_BLOCK = `
          <div class="footer__social">
            <span class="footer__social-label">Follow</span>
            <div class="footer__social-icons">
              <a href="https://www.linkedin.com/company/karman-advisory-singapore/" target="_blank" rel="noopener" aria-label="Karman on LinkedIn">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" xmlns="http://www.w3.org/2000/svg"><path d="M20.45 20.45h-3.55v-5.57c0-1.33-.03-3.04-1.85-3.04-1.85 0-2.14 1.45-2.14 2.94v5.67H9.36V9h3.41v1.56h.05c.48-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.45v6.29zM5.34 7.43a2.06 2.06 0 1 1 0-4.12 2.06 2.06 0 0 1 0 4.12zM7.12 20.45H3.56V9h3.56v11.45zM22.22 0H1.77C.79 0 0 .77 0 1.72v20.56C0 23.23.79 24 1.77 24h20.45c.98 0 1.78-.77 1.78-1.72V1.72C24 .77 23.2 0 22.22 0z"/></svg>
              </a>
            </div>
          </div>`;

function walk(dir, out = []) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (entry.name === 'node_modules' || entry.name === '.git') continue;
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) walk(full, out);
    else if (entry.isFile() && entry.name.endsWith('.html')) out.push(full);
  }
  return out;
}

const files = walk(ROOT);
let injected = 0, skipped = 0, failed = 0;

const badgesRegex = /<div class="footer__badges">[\s\S]*?<\/div>/;
// For Style B: match opening footer__brand div and find its closing </div>
const brandRegex = /<div class="footer__brand">([\s\S]*?)<\/div>(?=\s*<div class="footer__(?:col|links|grid))/;

for (const file of files) {
  let html = fs.readFileSync(file, 'utf8');
  if (html.includes(SENTINEL)) { skipped++; continue; }
  if (!html.includes('<footer class="footer">')) continue;

  // Try Style A first (badges block)
  if (badgesRegex.test(html)) {
    html = html.replace(badgesRegex, m => m + SOCIAL_BLOCK);
    fs.writeFileSync(file, html);
    injected++;
    continue;
  }

  // Try Style B: append before closing </div> of footer__brand
  const m = html.match(brandRegex);
  if (m) {
    const replacement = `<div class="footer__brand">${m[1]}${SOCIAL_BLOCK}\n        </div>`;
    html = html.replace(brandRegex, replacement);
    fs.writeFileSync(file, html);
    injected++;
    continue;
  }

  failed++;
  console.log('FAILED:', path.relative(ROOT, file));
}

console.log(`Injected:  ${injected}`);
console.log(`Skipped:   ${skipped} (already had it)`);
console.log(`Failed:    ${failed}`);
console.log(`Total:     ${files.length}`);
