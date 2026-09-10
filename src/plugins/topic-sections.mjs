import Slugger from 'github-slugger';
import { SECTION_IDS } from '../sections.mjs';

/**
 * Wraps each `##` block of a topic page in a <section> tagged with the template
 * slot it fills, and gives every heading an id plus an anchor link.
 *
 * The mapping comes from `sections:` in the file's frontmatter: an ordered list
 * of slot ids, one per `##` heading in the body. A page just leaves out the
 * slots it doesn't have, which is how the template degrades - nothing ever
 * renders an empty header.
 *
 * Two slots get an affordance appended:
 *   cram-sheet -> copy button (the cram sheet is the shareable unit)
 *   questions  -> a link to send in an interview question
 *
 * This is a Satteri hast plugin (Astro 7's default Markdown processor). Pass it
 * as a factory in `markdown.processor` so each document gets its own slugger.
 */


const el = (tagName, properties, children = []) => ({
  type: 'element',
  tagName,
  properties,
  children,
});

const text = (value) => ({ type: 'text', value });

/**
 * The anchor carries no text of its own - the "#" is drawn in CSS - so it stays
 * out of the heading's text content, which Astro collects for the headings list.
 */
const headingAnchor = (id) =>
  el('a', {
    className: ['heading-anchor'],
    href: `#${id}`,
    'aria-label': 'Link to this section',
  });

const cramSheetActions = () =>
  el('div', { className: ['section-actions'] }, [
    el(
      'button',
      {
        type: 'button',
        className: ['copy-button'],
        'data-copy-section': 'cram-sheet',
      },
      [text('Copy cram sheet')],
    ),
    el('span', {
      className: ['copy-status'],
      role: 'status',
      'aria-live': 'polite',
    }),
  ]);

const questionsActions = (submitUrl) =>
  el('div', { className: ['section-actions'] }, [
    el('a', { className: ['submit-link'], href: submitUrl }, [
      text('Send in a question you got asked'),
    ]),
  ]);

function checkDeclaredSections(declared, where) {
  for (const id of declared) {
    if (!SECTION_IDS.includes(id)) {
      throw new Error(
        `[topic-sections] ${where}: "${id}" is not one of the template sections (${SECTION_IDS.join(', ')}).`,
      );
    }
  }

  let previous = -1;
  for (const id of declared) {
    const at = SECTION_IDS.indexOf(id);
    if (at <= previous) {
      throw new Error(
        `[topic-sections] ${where}: sections are out of template order at "${id}". Expected order: ${SECTION_IDS.join(', ')}.`,
      );
    }
    previous = at;
  }
}

export function topicSections(options = {}) {
  const { submitUrl = '#' } = options;
  const slugger = new Slugger();

  return {
    name: 'topic-sections',

    element: {
      filter: ['h2', 'h3'],
      visit(node, ctx) {
        const existing = node.properties?.id;
        const id =
          typeof existing === 'string' ? existing : slugger.slug(ctx.textContent(node));
        ctx.setProperty(node, 'id', id);
        ctx.appendChild(node, headingAnchor(id));
      },
    },

    after(root, ctx) {
      const frontmatter = ctx.data?.astro?.frontmatter ?? {};
      const declared = frontmatter.sections;
      const where = ctx.fileURL ? ctx.fileURL.pathname.split('/').pop() : 'a content file';

      // Files that don't declare slots render as plain markdown, so stubs and
      // one-off pages don't have to opt in to the template.
      if (!Array.isArray(declared) || declared.length === 0) return;

      checkDeclaredSections(declared, where);

      // Split the top level of the document at each h2.
      const lead = [];
      const groups = [];
      for (const node of root.children) {
        if (node.type === 'element' && node.tagName === 'h2') {
          groups.push({ heading: node, body: [] });
        } else if (groups.length === 0) {
          lead.push(node);
        } else {
          groups[groups.length - 1].body.push(node);
        }
      }

      if (groups.length !== declared.length) {
        throw new Error(
          `[topic-sections] ${where}: frontmatter declares ${declared.length} section(s) but the body has ${groups.length} "##" heading(s). They have to line up one to one, in order.`,
        );
      }

      const sections = groups.map((group, i) => {
        const id = declared[i];
        const children = [group.heading, ...group.body];

        if (id === 'cram-sheet') children.push(cramSheetActions());
        if (id === 'questions') children.push(questionsActions(submitUrl));

        return el(
          'section',
          {
            className: ['topic-section', `topic-section--${id}`],
            'data-section': id,
          },
          children,
        );
      });

      ctx.replaceNode(root, { type: 'root', children: [...lead, ...sections] });
    },
  };
}

export default topicSections;
