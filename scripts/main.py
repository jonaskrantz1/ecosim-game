from pyodide.ffi import create_proxy
from js import window
from scripts.ecosystem import Ecosystem
from scripts.rendering import Renderer

# Bootstrap
eco = Ecosystem()
rnd = Renderer("game", eco)

def tick(_=None):
    eco.update()
    rnd.render()

# Run every 500ms
proxy = create_proxy(tick)
window.setInterval(proxy, 500)
