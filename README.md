# ChemE for Everyone

Working title. See `product-design-spec.md` for what this is and who it's for.

## Running it

```
npm install
npm run dev      # http://localhost:4321
npm run build    # content check, then static build into dist/
npm run preview  # serve dist/
```

Node 24. Astro 7, static output, no server.

## Adding a topic

Drop a markdown file in `src/content/equipment/` or `src/content/concepts/`.
The filename stem has to match the `slug`, and the folder has to match the
`category`. Nothing else gets touched - no template, no route, no nav.

```yaml
---
title: Compressors
slug: compressors
category: equipment
status: stub              # complete | draft | stub
summary: One line for cards and the meta description.
confidence: low           # high | medium | low - your own depth
reviewed_by: ""           # non-empty once an SME has checked it
updated: 2026-09-09
sections:                 # one entry per "##" heading, in template order
  - war-story
  - cram-sheet
---
```

`sections` maps your `##` headings onto the nine template slots, in order:

`war-story`, `school-vs-reality`, `what-it-does`, `what-matters`, `diagrams`,
`vocabulary`, `troubleshooting`, `cram-sheet`, `questions`

Your headings can say whatever you want - the mapping is positional, so the
slot ids never show up in the writing. Leave out the slots a page doesn't have
and they simply don't render. Two slots pick up an affordance automatically: the
cram sheet gets a copy button, and the questions section gets a submission link.

`npm run check:content` (which `npm run build` runs first) fails if the list and
the headings don't line up, so a broken page can't quietly vanish from a deploy.

## Where things live

```
src/
  sections.mjs                    the nine template slots - single source of truth
  site.config.ts                  name, origin, submission link
  content.config.ts               frontmatter schema
  content/equipment/*.md          the writing
  content/concepts/*.md
  layouts/BaseLayout.astro        html shell, meta and OG tags
  layouts/TopicLayout.astro       topic page chrome, cram-sheet copy script
  pages/[category]/[slug].astro   the topic route
  plugins/topic-sections.mjs      section wrapping, heading ids and anchors
  styles/global.css               everything, for now
scripts/check-content.mjs         pre-build content check
```

## Deploying

`.github/workflows/deploy.yml` builds and publishes to GitHub Pages on a push to
`main`. Before the first run, set Pages to deploy from GitHub Actions and put the
real URL in `SITE.origin`. Netlify and Cloudflare Pages both work with no config
if you'd rather - build `npm run build`, publish `dist/`.

## Build order

Steps 1-4 of `product-design-spec.md` section 12 are done. Next up: stub every
topic in section 8, then the landing page and `/cram`.
