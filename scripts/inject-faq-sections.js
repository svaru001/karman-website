const fs = require('fs');
const path = require('path');

const blogDir = path.join(__dirname, '../blog');
const dirs = fs.readdirSync(blogDir).filter(d =>
  fs.statSync(path.join(blogDir, d)).isDirectory()
);

let processed = 0, skipped = 0;

function extractFaqs(html) {
  for (const m of html.matchAll(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/g)) {
    try {
      const data = JSON.parse(m[1]);
      // Format 1: top-level FAQPage object
      if (data['@type'] === 'FAQPage') return data.mainEntity;
      // Format 2: FAQPage embedded inside @graph array
      if (Array.isArray(data['@graph'])) {
        for (const node of data['@graph']) {
          if (node['@type'] === 'FAQPage') return node.mainEntity;
        }
      }
    } catch {}
  }
  return null;
}

const esc = s => String(s)
  .replace(/&/g, '&amp;').replace(/</g, '&lt;')
  .replace(/>/g, '&gt;').replace(/"/g, '&quot;');

for (const dir of dirs) {
  const filePath = path.join(blogDir, dir, 'index.html');
  if (!fs.existsSync(filePath)) continue;

  let html = fs.readFileSync(filePath, 'utf8');

  if (html.includes('article-faq-section')) { skipped++; continue; }

  const faqs = extractFaqs(html);
  if (!faqs || !faqs.length) {
    console.log(`⚠ No FAQPage schema: ${dir}`);
    skipped++;
    continue;
  }

  const items = faqs.map(faq => `      <div class="faq-item">
        <button class="faq-question" aria-expanded="false">${esc(faq.name)}<span class="faq-icon">+</span></button>
        <div class="faq-answer"><p>${esc(faq.acceptedAnswer.text)}</p></div>
      </div>`).join('\n');

  const section = `
      <section class="article-faq-section" style="margin-top:56px;padding-top:0;">
        <h2>Frequently Asked Questions</h2>
        <div class="faq__grid" style="max-width:100%;margin-top:24px;">
${items}
        </div>
      </section>
`;

  if (!html.includes('</article>')) {
    console.log(`⚠ No </article>: ${dir}`);
    skipped++;
    continue;
  }

  html = html.replace('</article>', section + '\n    </article>');
  fs.writeFileSync(filePath, html);
  console.log(`✓ ${dir}`);
  processed++;
}

console.log(`\nDone: ${processed} injected, ${skipped} skipped`);
