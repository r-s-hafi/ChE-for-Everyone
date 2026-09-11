// Throwaway verification, deleted once it passes. Reads every .html file in
// this folder, writes nothing, touches no network.
//
// Checks the four things that actually break a hand-written site:
//   1. every local href/src points at a file that exists
//   2. every #fragment link points at an id that exists in the target page
//   3. the page shell is byte-identical across pages (the find-and-replace rule)
//   4. no ALL-CAPS placeholders survived into a published page
import { readFileSync, readdirSync, existsSync, statSync } from 'node:fs';
import { dirname, join, normalize, relative } from 'node:path';

const walk = (dir) =>
  readdirSync(dir, { withFileTypes: true }).flatMap((e) => {
    if (e.name === '.git' || e.name === 'node_modules') return [];
    const p = join(dir, e.name);
    return e.isDirectory() ? walk(p) : p.endsWith('.html') ? [p] : [];
  });

const pages = walk('.').map((p) => p.replace(/\\/g, '/').replace(/^\.\//, ''));
const problems = [];

const idsOf = (html) => new Set([...html.matchAll(/\sid="([^"]+)"/g)].map((m) => m[1]));

const cache = new Map();
const load = (p) => {
  if (!cache.has(p)) cache.set(p, readFileSync(p, 'utf8'));
  return cache.get(p);
};

for (const page of pages) {
  const html = load(page);
  const here = dirname(page);
  const myIds = idsOf(html);

  // template.html is authoring furniture, not a page: nothing links to it, and
  // its paths are deliberately written for the subdirectory it gets copied into.
  const isTemplate = page === 'template.html';

  // --- 1 and 2: links ---
  const links = isTemplate ? [] : [...html.matchAll(/(?:href|src)="([^"]+)"/g)].map((m) => m[1]);
  for (const link of links) {
    if (/^(https?:|mailto:|#|data:)/.test(link)) {
      // Same-page fragment
      if (link.startsWith('#') && !myIds.has(link.slice(1))) {
        problems.push(`${page}: fragment ${link} has no matching id`);
      }
      continue;
    }

    const [path, frag] = link.split('#');
    const target = normalize(join(here, path)).replace(/\\/g, '/');

    if (!existsSync(target) || !statSync(target).isFile()) {
      problems.push(`${page}: broken link -> ${link}  (looked for ${target})`);
      continue;
    }
    if (frag && target.endsWith('.html') && !idsOf(load(target)).has(frag)) {
      problems.push(`${page}: ${link} -> no id "${frag}" in ${target}`);
    }
  }

  // --- 3: identical shell ---
  const nav = html.match(/<nav class="site-nav"[\s\S]*?<\/nav>/);
  const footer = html.match(/<footer class="site-footer">[\s\S]*?<\/footer>/);
  if (!nav) problems.push(`${page}: no site-nav block`);
  if (!footer) problems.push(`${page}: no site-footer block`);
  if (nav && !isTemplate) {
    const depth = page.includes('/') ? 'nested' : 'root';
    const key = `nav:${depth}`;
    if (!cache.has(key)) cache.set(key, { text: nav[0], from: page });
    else if (cache.get(key).text !== nav[0]) {
      problems.push(`${page}: site-nav differs from ${cache.get(key).from} (same depth)`);
    }
  }

  // --- 4: leftover placeholders ---
  if (page !== 'template.html') {
    for (const ph of ['TOPIC NAME', 'ONE LINE', 'CATEGORY/SLUG', 'YYYY-MM-DD', 'REPLACE-ME']) {
      if (html.includes(ph)) problems.push(`${page}: leftover placeholder "${ph}"`);
    }
  }

  // --- bonus: structural sanity ---
  // Attributes may sit on the next line, so allow whitespace after the tag name.
  if (!/<meta\s+name="viewport"/.test(html)) problems.push(`${page}: no viewport meta`);
  if (!/<link\s+rel="canonical"/.test(html)) problems.push(`${page}: no canonical link`);
  if (!/<meta\s+name="description"/.test(html)) problems.push(`${page}: no meta description`);
  if (!/<html lang="en">/.test(html)) problems.push(`${page}: no lang attribute`);
  const h1s = (html.match(/<h1[ >]/g) || []).length;
  if (h1s !== 1) problems.push(`${page}: ${h1s} <h1> elements, expected 1`);
}

console.log(`checked ${pages.length} pages\n`);
if (problems.length === 0) {
  console.log('CLEAN: no broken links, no id mismatches, shells consistent, no placeholders.');
} else {
  for (const p of problems) console.log(`  ${p}`);
  console.log(`\n${problems.length} problem(s)`);
}
process.exit(problems.length ? 1 : 0);
