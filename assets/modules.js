/* Interactive modules — the registry and the mount loop.
 *
 * Zero modules exist today. This file is the slot they drop into, so the first
 * one is a two-line change here instead of an architecture decision later.
 *
 * The contract (see modules/README.md):
 *   - A module lives in modules/<slug>/ and exposes one mount function
 *   - mount(element, config) renders the module into that element
 *   - A page opts in with <div data-module="<slug>"></div>
 *   - Optional config rides along as a JSON attribute:
 *     <div data-module="pump-curve" data-config='{"npshr":true}'></div>
 *   - A slug with no registered module renders nothing. No error, no empty box.
 *
 * The hard rule: modules are progressive enhancement. Every page is complete
 * and useful with JavaScript off, because the content is the product. Nothing
 * in here may be load-bearing for reading a page.
 */

const MODULES = {
  // 'pump-curve': (element, config) => { ... },
};

function mountModules() {
  for (const element of document.querySelectorAll('[data-module]')) {
    const mount = MODULES[element.dataset.module];

    // Unregistered slug: leave the container empty. CSS hides empty
    // containers, so a page referencing a module that doesn't exist yet looks
    // exactly like a page that never referenced one.
    if (!mount) continue;

    let config = {};
    if (element.dataset.config) {
      try {
        config = JSON.parse(element.dataset.config);
      } catch (error) {
        // A malformed config shouldn't cost the reader the rest of the page.
        console.warn(`[modules] ${element.dataset.module}: bad data-config`, error);
        continue;
      }
    }

    try {
      mount(element, config);
    } catch (error) {
      console.warn(`[modules] ${element.dataset.module}: failed to mount`, error);
      element.replaceChildren();
    }
  }
}

mountModules();
