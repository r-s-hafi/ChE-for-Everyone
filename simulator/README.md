# simulator/ — reserved

Python simulation code goes here. It isn't in this repo yet, and it stays independent of the site. Don't couple them.

See [docs/pds.md](../docs/pds.md) section 7. The deferred decision: a static site can't run Python, so when a simulation needs to reach the browser the options are porting the math to JS, running Python in-browser via Pyodide, or standing up a small API. None of that needs deciding until there's a simulation worth shipping.

Until then, keep the Python package clean and importable, with its physics separated from any CLI or display code. That's what keeps all three paths open.
