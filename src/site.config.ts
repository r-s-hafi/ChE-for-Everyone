export { SECTIONS, SECTION_IDS } from './sections.mjs';

/**
 * Site-wide constants. Anything a human might want to change without going
 * hunting through components lives here.
 */
export const SITE = {
  /** Working title. See "Open questions" in product-design-spec.md. */
  name: 'ChemE for Everyone',
  /**
   * Canonical origin, used for canonical URLs and OG tags.
   * TODO: replace once the domain is decided.
   */
  origin: 'https://example.com',
  description:
    'What chemical engineering school skips and the plant expects you to know.',
  /**
   * Where "send in a question" points (page template, section 9).
   * A mailto is fine for v1 per the build order; swap for a form service later.
   * TODO: real address.
   */
  submitUrl: 'mailto:you@example.com?subject=Interview%20question',
} as const;
