# ChE for Everyone

What chemical engineering school skips and the plant expects you to know. Written first person by a process engineer at a refinery, aimed at students prepping for technical interviews.

Live at **https://r-s-hafi.github.io/ChE-for-Everyone/**

The build brief is [docs/pds.md](docs/pds.md). Read that first if you're wondering why something is the way it is.

---

## How this site is built

Hand-written HTML and one stylesheet. **No build step, no dependencies, no npm, nothing to install.** You edit a `.html` file, double-click it to see the result, commit, and the live site updates a minute later.

That's a deliberate choice, not a stopgap. The previous attempt at this site died in frontend scope with no pages written, and the content is the only thing here that can't be bought or copied. A toolchain you have to maintain is a way to spend evenings not writing about compressors.

### Preview

Double-click any `.html` file. That's it. There's no dev server to start, which is why every link on the site keeps its `.html` extension — a `file://` page has no server to resolve extensionless URLs.

### Deploy

Push to `main`. GitHub Pages is set to **Deploy from a branch** → `main` → `/ (root)`, so there's no workflow to run and nothing to break. `.nojekyll` tells Pages to serve the files as-is instead of running Jekyll over them.

### Optional: check your links

Broken links are the one thing that really bites a hand-written site, so there's a checker:

```
node check-site.mjs
```

It reads every `.html` file and reports broken links, `#anchor` links pointing at ids that don't exist, page shells that have drifted apart, and leftover `TOPIC NAME`-style placeholders. It needs Node but **no packages**, it writes nothing, and it is not part of building or deploying anything — the site works fine if you never run it, and deleting the file breaks nothing. Worth running before a push that touched more than one page.

---

## Adding a topic

1. Copy `template.html` to `equipment/<slug>.html` or `concepts/<slug>.html`.
2. Replace every ALL-CAPS placeholder in the file (title, description, canonical URL).
3. Write the sections you have. Delete the comment blocks for the ones you don't — an empty section should not exist, rather than sit there as a hollow heading.
4. Add a `<li>` to `equipment/index.html` or `concepts/index.html`, and to `index.html`. Drop `class="is-stub"` from the `<li>` once the page is actually written.
5. If you wrote a cram sheet, paste it into `cram.html` too. See the rules below.

Every `<h2>` and `<h3>` needs an `id` so it can be linked to directly. `template.html` shows the pattern, including the `#` anchor link that goes inside the heading.

### The nine sections

Same skeleton on every page, in this order, from [docs/pds.md](docs/pds.md) section 5:

1. Why do I care?
2. School vs. reality
3. What it actually does
4. What actually matters
5. Diagrams
6. Vocabulary
7. Troubleshooting
8. Cram sheet
9. Questions people actually get asked

These names describe what each section is *for*, not what it has to be *called* on the page. `equipment/pumps.html` opens its "why do I care" section with "I got asked this and completely blanked," which is better. Use your own wording; keep the `id` values as they are so links stay predictable across pages.

`equipment/pumps.html` is the reference implementation and the voice benchmark.

### Tracking how solid a page is

Line 2 of every topic page is a comment:

```html
<!-- status: complete | confidence: high | reviewed_by: (none yet) | updated: 2026-09-11 -->
```

This is [docs/pds.md](docs/pds.md) section 4's frontmatter, kept as author-facing metadata since there's no generator to read it. Accuracy is the entire product and your depth varies by topic, so keep `confidence` honest. Pages marked `low` say so in their body, in plain language, and should stay stubs until they've been researched and reviewed.

---

## Two maintenance rules

These are the price of having no build step. Both are cheap if you remember them and annoying if you don't.

**1. Editing a cram sheet means editing `cram.html` too.** That page is every cram sheet in one place, so the content is deliberately duplicated. A stale cram sheet is worse than no cram sheet, because someone is reading it the night before an interview.

**2. Changing the nav or footer is a find-and-replace across every `.html` file.** The page shell is intentionally identical in all of them — byte for byte — so a find-and-replace is safe. Don't hand-edit one page's shell into something slightly different, or you lose that guarantee.

Anything *visual* is exempt from rule 2. All styling lives in `assets/style.css`, so colors, type, spacing, and layout are always a one-file change.

---

## Layout

```
index.html              /                    landing: the premise, then the topic list
about.html              /about
cram.html               /cram                every cram sheet in one page
template.html                                copy this to start a topic; never linked
equipment/
  index.html            /equipment
  pumps.html            /equipment/pumps     complete
  ...                                        11 stubs
concepts/
  index.html            /concepts
  ...                                        6 stubs
assets/
  style.css                                  the only stylesheet
  modules.js                                 module registry, currently empty
  favicon.svg
content/literature/     [reserved]
modules/                [reserved]           one folder per interactive module
simulator/                                   Python simulation code, independent of the site
docs/pds.md                                  the build brief
TODO.txt                                     simulator gaps
instruct.md                                  simulator refactor notes
```

## Branches

`dev` is where work happens. `main` is what GitHub Pages publishes. Merge `dev` into `main` when you want the site to go live, rather than pushing straight to `main`.

The two branches used to be unrelated histories — the site and the simulator were effectively separate repos sharing one remote — and were merged into a single tree on 2026-09-11.

`simulator/` is deliberately uncoupled from the website. Nothing in the site imports it and nothing in it knows the site exists.

GitHub Pages serves `equipment/pumps.html` at `/equipment/pumps`, so the clean routes in [docs/pds.md](docs/pds.md) section 8 come free from naming files sensibly.

Links are **relative** (`../index.html` from a topic page), which means the site works unchanged on `file://`, on the GitHub Pages subpath, and on a custom domain later. Root-relative links would break on two of those three.

Reserved directories hold a `.gitkeep` and a README saying what goes there. `/literature`, `/jobs`, and `/simulations` are not built.

---

## Interactive modules

None exist. `assets/modules.js` is the slot they drop into: a registry object and a loop that mounts any `<div data-module="slug">` whose slug is registered, and silently ignores the ones that aren't. See [modules/README.md](modules/README.md) for the contract.

The hard rule is that modules are progressive enhancement. Every page has to be complete and useful with JavaScript off, because the content is the product.

---

## If the no-build approach stops paying off

It's a real tradeoff and it can expire. Two signals to watch for:

- You want to change the nav or footer and you put it off because it's 24 files.
- You notice `cram.html` has drifted out of date.

Either one means the duplication has started costing more than a toolchain would. Moving to a generator later is straightforward — Markdown converts cleanly from this HTML, and `assets/style.css` carries over untouched. Until then, this is less work.
