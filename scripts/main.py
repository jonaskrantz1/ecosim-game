print("▶ Loaded main.py")
import sys
sys.path.insert(0, "scripts")
print("PATHS:", sys.path)

from pyodide.ffi import create_proxy
from js import window

# Import from same folder, not top-level
from ecosystem import Ecosystem
from rendering import Renderer

eco = Ecosystem()
rnd = Renderer("game", eco)

def tick(_=None):
    eco.update()
    rnd.render()

proxy = create_proxy(tick)
window.setInterval(proxy, 500)
