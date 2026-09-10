// @ts-check
import { defineConfig } from 'astro/config';
import { satteri } from '@astrojs/markdown-satteri';
import { topicSections } from './src/plugins/topic-sections.mjs';
import { SITE } from './src/site.config.ts';

export default defineConfig({
  site: SITE.origin,
  // Static output. The site is 95% prose that never changes per request.
  output: 'static',
  trailingSlash: 'never',
  build: { format: 'directory' },
  markdown: {
    processor: satteri({
      // Passed as a factory so every document gets a fresh slugger.
      hastPlugins: [() => topicSections({ submitUrl: SITE.submitUrl })],
    }),
  },
});
