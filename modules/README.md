# modules/ — reserved

One folder per interactive module: a draggable pump curve, a distillation column where you change reflux ratio and tray count, a valve Cv calculator.

**Nothing is built yet.** This is a defined slot so the first module is a drop-in rather than an architecture decision. See [docs/pds.md](../docs/pds.md) section 6.

## The contract

- A module lives in `modules/<slug>/` and exposes one mount function.
- `mount(element, config)` renders the module into the given DOM element.
- Register it in `assets/modules.js`: `'pump-curve': mount`.
- A page opts in with `<div data-module="pump-curve"></div>`, optionally carrying `data-config='{"npshr":true}'`.
- A slug with no registered module renders nothing at all. No error, no empty box.

## The rule

Modules are progressive enhancement. Every page must be complete and useful with JavaScript off. The content is the product, and nothing in here may become load-bearing for reading a page.
