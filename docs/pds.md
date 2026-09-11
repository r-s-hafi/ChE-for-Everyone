# ChE for Everyone — Product Design Spec

Repo: https://github.com/r-s-hafi/ChE-for-Everyone

**What this doc is for:** the build brief. It defines what to build now and, more importantly, where future things plug in so they don't require a rewrite. Most of what's described here is an empty slot. That's the point.

---

## 1. The concept

A free resource that closes the gap between what chemical engineering students learn in school and what industry actually expects them to know.

Written first-person by a process engineer at a refinery. The value is direct plant experience, not textbook coverage.

**Primary use case:** a student prepping for a technical interview. They're anxious, short on time, and know their coursework didn't cover this.

**v1 scope:** oil, gas, and refining. Deliberately narrow.

---

## 2. Design principles

1. **Content is the product.** The site exists to deliver writing that only this author can produce. Everything else is plumbing.
2. **Boring frontend.** Readable typography, working navigation, mobile-friendly. No design system, no animation, no component library. The last attempt died on frontend scope.
3. **Every future feature is a slot, not a build.** Define where things go. Don't build them.
4. **Adding content is adding a file.** Never edit a template to publish a page.
5. **Nothing generated as content.** AI writes scaffolding, not prose. A page a model could have written has no reason to exist.

---

## 3. Repo layout

```
/
  content/
    equipment/          # pumps.md, compressors.md, ...
    concepts/           # troubleshooting method, reading a P&ID, ...
    literature/         # [reserved — empty]
  modules/              # [reserved] interactive widgets, one folder each
  simulator/            # existing Python simulation code
  site/                 # the web app
    templates/
    static/
  docs/
    pds.md              # this file
```

Reserved directories get a `.gitkeep` and a one-line README saying what goes there. Visible slots, no code.

Delete the stray `self.v_frac` file in the repo root.

> **Build note, 2026-09-11.** Built with no generator, so the `content/` and `site/` split has nothing to describe — the HTML files are both, and they live at the repo root because that's what GitHub Pages serves. The reserved directories above exist as specified. `simulator/` holds the real Python code: it and the site were unrelated histories sharing one remote, and were merged into this single tree. `self.v_frac` was an empty file on the old `dev` branch and is now deleted. See `README.md`.

---

## 4. Content model

Markdown with YAML frontmatter. One file per topic.

```yaml
---
title: Pumps
slug: pumps
category: equipment        # equipment | concepts | literature
status: complete           # complete | draft | stub
summary: One line for indexes and meta description.
confidence: high           # high | medium | low
reviewed_by: ""            # set when an SME has checked it
modules: []                # slugs of interactive modules — empty for now
updated: 2026-09-11
---
```

**`status`** drives rendering. Stubs render a real page saying it isn't written yet, so the full topic list is visible from day one and the gaps are obvious.

**`confidence` and `reviewed_by`** exist because accuracy is the whole product. The author's depth varies by topic. Pumps and tanks are strong; compressors and fired heaters will need research and review. Track it honestly.

**`modules`** is the extension point for section 6. Ships empty. The template ignores it until there's something to render.

---

## 5. Page template

Nine sections, same skeleton every page. Sections that are empty in the frontmatter don't render at all, so early pages don't show hollow headers.

1. Why do I care? — first-person hook, a real question or failure
2. School vs. reality
3. What it actually does — short mental model
4. What actually matters — the core
5. Diagrams — inline where relevant
6. Vocabulary — table
7. Troubleshooting — symptom, then method
8. Cram sheet — bullets, screenshot-friendly
9. Questions people actually get asked

`content/equipment/pumps.md` is the reference implementation and the voice benchmark. Render it correctly and the template is proven.

---

## 6. Module system (slot, don't build)

Eventually each equipment page gets interactive pieces: a draggable pump curve, a distillation column where you change reflux ratio and tray count, a valve Cv calculator.

**Define the contract now, build nothing.**

- A module is a self-contained folder under `modules/<slug>/`
- It exposes one mount function: given a DOM element and a config object, it renders itself
- A page opts in by listing the slug in its `modules:` frontmatter
- The template renders a container div for each listed module; if the module doesn't exist, nothing renders

That's the whole spec. One registry file mapping slug to module, and a loop in the template. Maybe thirty lines. Write those thirty lines now so the first module is a drop-in later.

**Rule:** modules are progressive enhancement. Every page must be complete and useful with JavaScript off. The content is the product.

---

## 7. Simulator

`simulator/` already has Python simulation code and stays independent of the site for now. Don't couple them.

The real decision, deferred: a static site can't run Python. When simulations need to reach the browser, the options are porting the math to JS, running Python in-browser via Pyodide, or standing up a small API. Each has real tradeoffs and none needs deciding until there's a simulation worth shipping.

Until then: keep the Python package clean and importable, with its physics separated from any CLI or display code. That's what makes any of the three paths viable later.

---

## 8. Routes

```
/                      Landing
/equipment             Index
/equipment/<slug>      Topic page
/concepts              Index
/concepts/<slug>       Topic page
/cram                  Every cram sheet on one page
/about                 Who wrote this and why
```

Reserved, not built: `/literature`, `/jobs`, `/simulations`.

**Landing page** does one job: convince a stressed student this is worth twenty minutes. The premise, then the topic list. No feature grid.

**`/cram`** is deliberate. Someone with an hour left wants everything in one scrollable place.

---

## 9. Stack

Static site generator. Astro or Eleventy. Markdown content collections, one template, output is plain HTML files.

> **Build note, 2026-09-11.** Neither, for now. Phase 1 is hand-written HTML and one stylesheet, no build step and no dependencies, deployed straight from `main`. The reasoning, the two maintenance costs it accepts, and the specific signals that would justify moving to a generator are in `README.md`.

Why static:
- The content doesn't change per request, so a server buys nothing
- SEO is the distribution channel — students google "deadhead point pump curve"
- Free hosting that survives a Reddit spike
- Git is the CMS

The module system above works fine on static hosting since modules are client-side JS loaded per page.

Non-negotiables: mobile-first, fast on bad connections, readable line length, dark mode, per-page meta from frontmatter, anchor links on headings.

---

## 10. Build phases

**Phase 1 — the only one that matters now**
1. Stack, build, deploy. Empty site live on a real URL.
2. Content collection and frontmatter schema.
3. Page template, degrading gracefully.
4. Render `pumps.md` end to end.
5. Stub every topic. Nav complete, gaps visible.
6. Landing page, `/cram`, `/about`.
7. Module registry and mount loop. Zero modules.

Stop there. Phase 1 is done when pumps looks right on a phone.

**Later phases, in rough order:** diagrams for pumps → write compressors, heat exchangers, valves → first interactive module → literature section → simulations → job board.

Each of those is one PR against an existing slot, not an architecture change. That's the test of whether this spec worked.

---

## 11. Topics to stub

**Equipment:** pumps *(complete)*, control valves, heat exchangers, distillation columns, tanks and vessels, compressors, fired heaters, piping and hydraulics, relief systems and PSVs, filters and strainers, steam systems, instrumentation basics

**Concepts:** the troubleshooting method, how to read a P&ID, what a process engineer actually does, working with operations and maintenance, practical process safety, interview prep strategy

---

## 12. Explicitly not now

No accounts, payments, CMS, comments, search, job board, or analytics beyond something simple. No monetization scaffolding of any kind.

Monetization is plausible eventually — sponsored content, a curated job board, paid mock interviews — and none of it works without a good free resource and real traffic. Building for it now is how this stalls again.

---

## 13. Open questions

- Domain name
- Whether to name the employer in the war story
- Who reviews the machinery-heavy content before it goes live
- Whether stub pages are public at launch

---

## 14. The failure mode

The build is the fun part and the content is the moat. Last attempt died in frontend scope with no pages written.

Phase 1, then stop and go write compressors.
