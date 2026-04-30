#!/usr/bin/env node
/* Inject Google Analytics 4 tag into every HTML page right after <head>. */

const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const GA_ID = 'G-DVKN5K8KSD';
const SENTINEL = `id=${GA_ID}`;

const SNIPPET = `
  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=${GA_ID}"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', '${GA_ID}');
  </script>
`;

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

for (const file of files) {
  const html = fs.readFileSync(file, 'utf8');
  if (html.includes(SENTINEL)) { skipped++; continue; }
  const headOpen = html.match(/<head[^>]*>/i);
  if (!headOpen) { failed++; console.log('NO <head>:', path.relative(ROOT, file)); continue; }
  const idx = headOpen.index + headOpen[0].length;
  const next = html.slice(0, idx) + SNIPPET + html.slice(idx);
  fs.writeFileSync(file, next);
  injected++;
}

console.log(`Injected:  ${injected}`);
console.log(`Skipped:   ${skipped} (already had GA)`);
console.log(`Failed:    ${failed}`);
console.log(`Total:     ${files.length}`);
