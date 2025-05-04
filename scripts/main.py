from pyodide.http import open_url
from pyodide.ffi import create_proxy
from js import window, document

# Dynamically load existing modules
def _load_and_exec(path):
    src = open_url(path).read()
    exec(src, globals())

for mod in ("utils.py", "ecosystem.py", "rendering.py"):
    _load_and_exec(f"scripts/{mod}")

# Dynamically load UI modules (ensure these files exist!)
for mod in ("ui/button.py", "ui/toolbar.py", "ui/palette.py"):
    _load_and_exec(f"scripts/{mod}")

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
