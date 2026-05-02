#!/usr/bin/env node
/**
 * Move the LinkedIn icon inline with the ACRA/MAS badge pills.
 * - Style A pages (have footer__badges): append LinkedIn anchor inside footer__badges, delete footer__social div.
 * - Style B pages (no footer__badges): replace footer__social div with a footer__badges div containing only the LinkedIn anchor.
 */
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');

const LINK_ANCHOR = '<a class="footer__social-link" href="https://www.linkedin.com/company/karman-advisory-singapore/" target="_blank" rel="noopener" aria-label="Karman on LinkedIn"><svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor" xmlns="http://www.w3.org/2000/svg"><path d="M20.45 20.45h-3.55v-5.57c0-1.33-.03-3.04-1.85-3.04-1.85 0-2.14 1.45-2.14 2.94v5.67H9.36V9h3.41v1.56h.05c.48-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.45v6.29zM5.34 7.43a2.06 2.06 0 1 1 0-4.12 2.06 2.06 0 0 1 0 4.12zM7.12 20.45H3.56V9h3.56v11.45zM22.22 0H1.77C.79 0 0 .77 0 1.72v20.56C0 23.23.79 24 1.77 24h20.45c.98 0 1.78-.77 1.78-1.72V1.72C24 .77 23.2 0 22.22 0z"/></svg></a>';

const SOCIAL_BLOCK_RE = /[ \t]*<div class="footer__social">.*?<\/div><\/div>\n?/;
const BADGES_CLOSE_RE = /(<div class="footer__badges">[\s\S]*?)<\/div>/;

function walk(dir, files = []) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (entry.name === 'node_modules' || entry.name.startsWith('.')) continue;
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) walk(full, files);
    else if (entry.name.endsWith('.html')) files.push(full);
  }
  return files;
}

let changed = 0, skipped = 0;
for (const file of walk(ROOT)) {
  let html = fs.readFileSync(file, 'utf8');
  if (!html.includes('footer__social')) continue;

  const hasBadges = /<div class="footer__badges">/.test(html);
  let next;
  if (hasBadges) {
    // Append LinkedIn anchor to footer__badges and remove footer__social block.
    next = html.replace(BADGES_CLOSE_RE, `$1  ${LINK_ANCHOR}\n          </div>`);
    next = next.replace(SOCIAL_BLOCK_RE, '');
  } else {
    // Replace footer__social with a footer__badges containing only the LinkedIn anchor.
    next = html.replace(SOCIAL_BLOCK_RE, `          <div class="footer__badges">${LINK_ANCHOR}</div>\n`);
  }

  if (next !== html) {
    fs.writeFileSync(file, next);
    changed++;
  } else {
    skipped++;
    console.warn('No change:', path.relative(ROOT, file));
  }
}
console.log(`Updated ${changed} files; ${skipped} unchanged.`);
