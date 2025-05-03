# ────────────────────────────────────────────────────────────
# Dynamically load utils.py, ecosystem.py, rendering.py into this namespace
# ────────────────────────────────────────────────────────────

from pyodide.http import open_url

def _load_and_exec(path):
    # open_url().read() returns a Python string
    src = open_url(path).read()
    exec(src, globals())

# now load each module in order
for mod in ("utils.py", "ecosystem.py", "rendering.py"):
    _load_and_exec(f"scripts/{mod}")

# ────────────────────────────────────────────────────────────
# Now everything from those modules is in global scope: 
#   load_json, perlin, Plant, Ecosystem, Renderer, etc.
# ────────────────────────────────────────────────────────────

from pyodide.ffi import create_proxy
from js import window

# Bootstrapping
eco = Ecosystem()
rnd = Renderer("game", eco)

def tick(_=None):
    eco.update()
    rnd.render()

proxy = create_proxy(tick)
window.setInterval(proxy, 500)
