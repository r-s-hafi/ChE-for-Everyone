import { defineCollection } from 'astro:content';
import { z } from 'zod';
import { glob } from 'astro/loaders';
import { SECTION_IDS } from './sections.mjs';

const sectionIds = SECTION_IDS as [string, ...string[]];

/**
 * Shared frontmatter for every topic page. Adding a topic means adding a
 * markdown file - no template ever gets touched.
 */
const topicSchema = z.object({
  title: z.string(),
  slug: z.string(),
  category: z.enum(['equipment', 'concepts']),

  /** Drives the UI. Stubs render a "not written yet" page, never a 404. */
  status: z.enum(['complete', 'draft', 'stub']),

  /** One line, used for cards and the meta description. */
  summary: z.string(),

  /**
   * The author's own depth on this topic. Accuracy is the product, so a page
   * where he's extrapolating should say so. Author-facing metadata.
   */
  confidence: z.enum(['high', 'medium', 'low']),

  /** Non-empty once a subject-matter expert has checked it. */
  reviewed_by: z.string().default(''),

  updated: z.coerce.date(),

  /**
   * Which template slots this file fills, in order, one per "##" heading.
   * Leave a slot out and it just doesn't render. See
   * src/plugins/rehype-topic-sections.mjs.
   */
  sections: z.array(z.enum(sectionIds)).default([]),
});

export type TopicFrontmatter = z.infer<typeof topicSchema>;

const equipment = defineCollection({
  loader: glob({ base: './src/content/equipment', pattern: '**/*.md' }),
  schema: topicSchema,
});

const concepts = defineCollection({
  loader: glob({ base: './src/content/concepts', pattern: '**/*.md' }),
  schema: topicSchema,
});

export const collections = { equipment, concepts };
