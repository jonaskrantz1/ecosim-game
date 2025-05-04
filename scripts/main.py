from pyodide.http import open_url
from pyodide.ffi import create_proxy
from js import window, document

# Dynamically load utils, ecosystem, rendering modules
def _load_and_exec(path):
    src = open_url(path).read()
    exec(src, globals())

for mod in ("utils.py", "ecosystem.py", "rendering.py"):
    _load_and_exec(f"scripts/{mod}")

# Import Toolbar UI
_load_and_exec("scripts/ui/button.py")
_load_and_exec("scripts/ui/toolbar.py")
_load_and_exec("scripts/ui/palette.py")  # placeholder for palette later

# Initialize ecosystem and renderer
eco = Ecosystem()
rnd = Renderer("game", eco)

# Initialize Toolbar UI
toolbar = Toolbar()
toolbar.render()

# Main update loop
def tick(_=None):
    eco.update()
    rnd.render()

proxy = create_proxy(tick)
window.setInterval(proxy, 500)
