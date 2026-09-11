# simulator/

Python process simulation code. **It stays independent of the site** — nothing in the website imports from here, and nothing here knows the website exists. Don't couple them. See [docs/pds.md](../docs/pds.md) section 7.

## What's here

| File | Contents |
| --- | --- |
| `models.py` | `component` and `stream` |
| `base.py` | `UnitOp` abstract base class |
| `unit_ops.py` | `pump`, `heat_exchanger`, and stubs for `compressor`, `flash_drum`, `distillation_column` |
| `components.py` | the `component_db` dict |
| `nist_scraper.py` | builds the component database |
| `test_unit_ops.py` | tests |

```
pytest -v
```

Known gaps are tracked in [TODO.txt](../TODO.txt): `Cp` is currently assumed constant and needs integrating, VLE streams aren't handled, the heat exchanger needs validation, and the pump class needs a temperature rise for inefficiency.

## The deferred decision

A static site can't run Python. When a simulation needs to reach the browser, the options are porting the math to JavaScript, running Python in-browser via Pyodide, or standing up a small API. Each has real tradeoffs and none of it needs deciding until there's a simulation worth shipping.

Until then, keep this package clean and importable, with the physics separated from any CLI or display code. That's what keeps all three paths open.

Note that these `.py` files sit in the same repository that GitHub Pages publishes, so they're reachable over HTTP as well as on GitHub. The repository is public either way, so this exposes nothing new — but don't put a credential in here.
