/**
 * Pre-build sanity check on the content files.
 *
 * Astro logs a render error and carries on if a page's sections don't line up,
 * which means a broken page can quietly vanish from a deploy. This runs first
 * and exits non-zero instead.
 *
 * Checks, per file:
 *   - the `sections:` list matches the "##" headings one to one, in order
 *   - every declared section id is a real template slot, in template order
 *   - the frontmatter slug matches the filename and the category matches the
 *     folder, so URLs stay predictable
 */
import { readdir, readFile } from 'node:fs/promises';
import { join, relative, sep } from 'node:path';
import { fileURLToPath } from 'node:url';
import { SECTION_IDS } from '../src/sections.mjs';

const root = fileURLToPath(new URL('..', import.meta.url));
const contentDir = join(root, 'src', 'content');

const problems = [];

/** Enough YAML for the frontmatter this project uses. */
function readFrontmatter(source) {
  const match = source.match(/^---\r?\n([\s\S]*?)\r?\n---/);
  if (!match) return null;

  const data = {};
  let listKey = null;

  for (const line of match[1].split(/\r?\n/)) {
    const item = line.match(/^\s+-\s+(.*)$/);
    if (item && listKey) {
      data[listKey].push(item[1].trim());
      continue;
    }

    const pair = line.match(/^([A-Za-z_][\w-]*):\s*(.*)$/);
    if (!pair) continue;

    const [, key, rawValue] = pair;
    const value = rawValue.trim();
    if (value === '') {
      listKey = key;
      data[key] = [];
    } else {
      listKey = null;
      data[key] = value.replace(/^["'](.*)["']$/, '$1');
    }
  }

  return data;
}

function checkFile(path, source) {
  const where = relative(root, path).split(sep).join('/');
  const fail = (message) => problems.push(`${where}: ${message}`);

  const frontmatter = readFrontmatter(source);
  if (!frontmatter) {
    fail('no frontmatter block.');
    return;
  }

  const [, category, file] = where.split('/').slice(-3);
  const stem = file.replace(/\.md$/, '');

  if (frontmatter.category !== category) {
    fail(`category is "${frontmatter.category}" but the file sits in ${category}/.`);
  }
  if (frontmatter.slug !== stem) {
    fail(`slug is "${frontmatter.slug}" but the file is named ${file}.`);
  }

  const declared = frontmatter.sections ?? [];
  if (declared.length === 0) return;

  const body = source.slice(source.indexOf('\n---', 3) + 4);
  const headings = body.match(/^## .*$/gm) ?? [];

  if (declared.length !== headings.length) {
    fail(
      `frontmatter declares ${declared.length} section(s) but the body has ${headings.length} "##" heading(s).`,
    );
  }

  let previous = -1;
  for (const id of declared) {
    const at = SECTION_IDS.indexOf(id);
    if (at === -1) {
      fail(`"${id}" is not one of the template sections.`);
    } else if (at <= previous) {
      fail(`sections are out of template order at "${id}".`);
    }
    previous = Math.max(previous, at);
  }
}

const files = await readdir(contentDir, { recursive: true, withFileTypes: true });
const markdown = files.filter((entry) => entry.isFile() && entry.name.endsWith('.md'));

for (const entry of markdown) {
  const path = join(entry.parentPath ?? entry.path, entry.name);
  checkFile(path, await readFile(path, 'utf8'));
}

if (problems.length > 0) {
  console.error(`\nContent check failed:\n${problems.map((p) => `  - ${p}`).join('\n')}\n`);
  console.error(`Template sections, in order: ${SECTION_IDS.join(', ')}\n`);
  process.exit(1);
}

console.log(`Content check passed (${markdown.length} file(s)).`);
