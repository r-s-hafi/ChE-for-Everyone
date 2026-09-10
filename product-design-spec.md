# Product Design Spec

**Working title:** ChemE for Everyone *(name not final — see Open Questions)*

**Purpose of this doc:** hand to Claude Code as the build brief. It describes what the site is, who it's for, how content is structured, and what to scaffold. Most content pages will be empty stubs at first. That's intentional.

---

## 1. What this is

A free web resource that closes the gap between what chemical engineering students learn in school and what they're actually expected to know in industry.

It is not a textbook. It is not a course. It's the thing a student reads the night before a technical interview, written by someone a few years ahead of them who has been in the room.

**Author:** one person, a process engineer at a refinery. All content is first-person, based on direct plant experience.

**Scope for v1:** oil, gas, and refining. Explicitly narrow. Not a general chemE resource. Broadening (pharma, bio, specialty chem) is a later-stage decision, not a v1 goal.

---

## 2. Who it's for and when they use it

**Primary user:** a chemical engineering junior or senior with a technical interview coming up. They have a few hours, they're anxious, and they know their coursework didn't prepare them for questions about real equipment.

**The moment:** 11pm, night before or few days before the interview, on a laptop or phone.

**Secondary user:** a new hire or co-op in their first weeks who keeps hearing terms nobody explains.

**What they want:** to not get caught out. To sound like they've been around this stuff.

Every design decision resolves against that moment. If a feature doesn't help someone cramming at 11pm, it doesn't belong in v1.

---

## 3. Why this exists when ChatGPT exists

This is the central design constraint. A general model can already explain how a pump works. The site is only worth building if every page delivers something a model can't:

1. **War stories.** Real interview questions the author was asked, real failures, real conversations on the plant. First-person and specific.
2. **What interviewers are actually testing.** Not just the answer, but why they're asking.
3. **Curation.** A student doesn't know what they don't know, so "explain pumps" gets them a firehose. This site gives them the specific things that actually come up.
4. **Vetted visuals.** Correct, annotated diagrams the author has checked. Generated images are often subtly wrong in ways a novice can't catch. This matters most for students at schools without plant tours or industry connections.

**Implication for Claude Code:** do not generate body content. Content is authored by a human from direct experience. AI assistance is for scaffolding, layout, components, and diagrams — not prose.

---

## 4. Voice and tone

The author's voice is conversational, direct, a little self-deprecating. Any generated copy (nav labels, empty states, meta descriptions, 404 page) must match it.

**Do:**
- Contractions, plain words, second person
- Longer conversational sentences with parentheticals
- Hedges where honest: "in my experience," "that might just be a me thing"
- Admit gaps: "I'm a process guy, not a machinery guy"

**Don't:**
- Em-dash asides
- "X isn't Y, it's Z" constructions
- Punchy one-line fragments closing every section
- Bolded lead-ins on every bullet
- "Here's the thing," "worth noting," "the key insight is"
- Corporate or textbook register

See `content/equipment/pumps.md` as the reference. It's the finished example and the voice benchmark.

---

## 5. Page template

Every equipment page follows the same skeleton. Consistency is a feature: readers learn the pattern, and the author writes faster.

| # | Section | Purpose |
|---|---|---|
| 1 | **War story** | First-person hook. A real question, failure, or moment. Establishes credibility immediately. |
| 2 | **School vs. reality** | What the course covered vs. what the job needs. The thesis of the whole site, restated per topic. |
| 3 | **What it actually does** | Minimum viable mental model. Short. No derivations. |
| 4 | **The stuff that actually matters** | The core. Four to six subsections on what drives real behavior. |
| 5 | **Diagrams** | Inline where relevant, not batched at the end. |
| 6 | **Vocabulary** | Table. Terms used in conversation with no explanation. |
| 7 | **Troubleshooting** | Common symptom, then a repeatable method, then how to reason through it. |
| 8 | **Cram sheet** | Bulleted recap. Screenshot-friendly. This is the shareable unit. |
| 9 | **Questions people actually get asked** | The real question plus what's being tested. Grows over time via reader submissions. |

Sections 4, 7, and 9 carry the value. 3 and 6 can be thin.

**Rendering notes:**
- Sections 2 and 9 may be short or absent on early pages. Template must degrade gracefully — no empty headers.
- Section 8 needs a copy or screenshot affordance. It's the distribution mechanism.
- Section 9 needs a submission link.

---

## 6. Content model

Content lives in markdown files. One file per topic. Adding a topic means adding a file, never touching a template.

```
content/
  equipment/
    pumps.md
    compressors.md
    heat-exchangers.md
    ...
  concepts/
    troubleshooting-method.md
    ...
```

**Frontmatter:**

```yaml
---
title: Pumps
slug: pumps
category: equipment
status: complete        # complete | draft | stub
summary: One line for cards and meta description.
confidence: high        # high | medium | low — author's own depth
reviewed_by: ""         # non-empty when a subject-matter expert has checked it
updated: 2026-09-09
---
```

`status` drives the UI. Stubs render as a "not written yet" page rather than 404, so the nav is complete from day one and the author can see the gaps.

`confidence` and `reviewed_by` exist because accuracy is the entire product. A page where the author is extrapolating should be marked, and pages covering mechanical detail should be flagged for expert review before they're treated as done. This is metadata for the author, not necessarily surfaced to readers.

---

## 7. Site structure

```
/                          Landing
/equipment                 Index of equipment pages
/equipment/<slug>          Page (template above)
/concepts                  Index of cross-cutting topics
/concepts/<slug>           Page
/cram                      All cram sheets on one page
/about                     Who wrote this and why
/submit                    Submit an interview question
```

**Landing page.** Must do one job: convince a stressed student this is worth their next twenty minutes. Lead with the war story premise and the school-vs-reality thesis. No feature grid, no marketing copy. Straight to a clear list of topics.

**`/cram`** is a deliberate feature. Someone with one hour left wants every cram sheet in one scrollable place.

**Stub pages.** Render the title, the standard skeleton headers greyed out, and a short honest line in the author's voice about it not being written yet. Optionally a "tell me to prioritize this" link.

---

## 8. Topic list to scaffold

Create a stub for each. Only pumps has content.

**Equipment**
- Pumps — *complete*
- Control valves
- Heat exchangers
- Distillation columns
- Tanks and vessels
- Compressors
- Fired heaters
- Piping and hydraulics
- Relief systems and PSVs
- Filters and strainers
- Steam systems
- Instrumentation basics

**Concepts**
- The troubleshooting method
- How to read a P&ID
- What a process engineer actually does day to day
- Working with operations and maintenance
- Process safety, the practical version
- Interview prep strategy

Author's own depth varies a lot across these. Pumps and tanks are strongest; compressors and fired heaters will need research and expert review. That's what the `confidence` field is for.

---

## 9. Visuals

The second differentiator, and the most labor-intensive part. Do not gate the site on complete illustration.

**Approach:** hand-authored SVG, checked into the repo, stored per-topic. Not generated images. They need to be correct, legible on a phone, and dark-mode safe.

**Requirements:**
- Inline SVG so it themes with CSS and stays crisp
- Readable at ~360px wide
- Use `currentColor` or CSS variables, no hardcoded blacks
- Alt text and a caption on every diagram
- A consistent visual language across topics (same annotation style, same type scale)

**Highest-value diagrams for the pumps page:**
1. Centrifugal curve with deadhead, BEP, runout, plus system curve and operating point
2. PD curve alongside it, showing near-vertical behavior
3. Volute cross-section showing even pressure at BEP vs. lopsided off-BEP — this one is hard to picture from text and is the best candidate for the first real illustration

**Interactive, later:** a curve explorer where the reader drags the system curve and watches the operating point move. Distillation will want a reflux-ratio and tray-count widget. Both are v2. Build the SVG pipeline first.

---

## 10. Tech

**Recommendation: static site generator, deployed static.** Astro or similar. Markdown content collections, component islands only where something needs interactivity.

Rationale:
- The site is 95% static content. A server buys nothing and costs money.
- SEO is the primary distribution channel — students will google "deadhead point pump curve" — so pre-rendered HTML matters.
- Content-as-markdown keeps the author writing in a text file instead of a CMS.
- Free hosting, and it can't fall over if a Reddit post lands.

**Alternative:** the author knows FastAPI + Jinja + HTMX and could ship that faster. Viable, but it means running a server for content that never changes per-request. Worth 20 minutes of thought before committing, not more.

**Non-negotiables regardless of stack:**
- Mobile-first. Half the traffic will be phones.
- Fast on bad connections. No heavy JS for reading text.
- Dark mode.
- Clean typography and comfortable line length. This is long-form reading.
- Per-page meta tags and OG images driven from frontmatter.
- Anchor links on every heading, so people can link straight to a section.

---

## 11. Explicitly not in v1

- Accounts, login, user data
- Payments or paywalls
- A CMS or admin UI — markdown files and git are the CMS
- Comments
- A job board
- Ads or sponsorship placements
- Search (revisit once there are ~10 real pages)
- Analytics beyond something simple and privacy-respecting

Monetization is a real long-term idea (sponsored content, a curated job board matching prepared candidates to real roles, paid mock interviews) but none of it works without a genuinely good free resource and real traffic first. Building any of it now is a distraction. Do not scaffold for it.

---

## 12. Build order

1. Repo, stack, deploy pipeline. Get an empty site live on a real URL.
2. Content collection, frontmatter schema, markdown rendering.
3. Page template implementing the nine sections, degrading gracefully.
4. Render `pumps.md` end to end. This is the proof the template works.
5. Stub every topic from section 8. Nav complete, gaps visible.
6. Landing page and `/cram`.
7. Typography, mobile, dark mode.
8. First SVGs for the pumps page.
9. Submission form for section 9 (can be a plain mailto or form service).

Step 4 is the milestone. Everything before it is plumbing; everything after it is repetition.

---

## 13. Open questions

- **Name and domain.** Working title only. Needs deciding before launch.
- **Whether to name the employer** in the war story. Currently generic. More credible if named, but it's a public page and worth thinking about.
- **Expert review path.** Who checks the machinery-heavy sections before they go live. Accuracy is the whole product, and a knowledgeable reader will test the numbers.
- **How reader-submitted questions get vetted** before they land in section 9.
- **Whether stub pages are public** at launch or hidden until written. Public shows scope and invites feedback; hidden looks more finished.

---

## 14. The failure mode to avoid

The build is the fun part. The content is the moat. It is very easy to spend three nights on an elegant scaffold and zero nights writing the thing that makes anyone visit.

Get to step 4, then stop building and go write compressors.
