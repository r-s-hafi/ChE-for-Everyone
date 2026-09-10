/**
 * The nine sections of the topic page template, in order.
 *
 * Single source of truth: the markdown plugin, the frontmatter schema, and the
 * pre-build content check all read this list. Plain JS so the standalone check
 * script can import it without a build step.
 */
export const SECTIONS = [
  { id: 'war-story', label: 'War story' },
  { id: 'school-vs-reality', label: 'School vs. reality' },
  { id: 'what-it-does', label: 'What it actually does' },
  { id: 'what-matters', label: 'The stuff that actually matters' },
  { id: 'diagrams', label: 'Diagrams' },
  { id: 'vocabulary', label: 'Vocabulary' },
  { id: 'troubleshooting', label: 'Troubleshooting' },
  { id: 'cram-sheet', label: 'Cram sheet' },
  { id: 'questions', label: 'Questions people actually get asked' },
];

/** Slot ids in template order. */
export const SECTION_IDS = SECTIONS.map((section) => section.id);
