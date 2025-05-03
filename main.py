import json
from pyodide.http import open_url
from js import document
from js import window

# ————————————————————————————————————————————————————————————————————————————
# Helper to load JSON
def load_json(path):
    resp = open_url(path)
    return json.loads(resp.read())

# ————————————————————————————————————————————————————————————————————————————
# Plant & Ecosystem logic
class Plant:
    def __init__(self, attrs, x, y):
        self.species = attrs["species"]
        self.x = x
        self.y = y
        self.age = 0
        self.attrs = attrs

class Ecosystem:
    def __init__(self):
        data = load_json("data/plants.json")
        self.plants = [
            Plant(attrs, (i*3) % 64, (i*5) % 48)
            for i, attrs in enumerate(data)
        ]

    def update(self):
        for p in self.plants:
            p.age += 1

# ————————————————————————————————————————————————————————————————————————————
# Renderer
class Renderer:
    def __init__(self, canvas_id, ecosystem):
        can = document.getElementById(canvas_id)
        self.ctx = can.getContext("2d")
        self.eco = ecosystem
        self.tile = 16
        self.colors = {
            "Grass": "#4CAF50",
            "Bush":  "#8BC34A",
            "Tree":  "#388E3C",
        }

    def render(self):
        # clear
        self.ctx.clearRect(0, 0, 1024, 768)
        # draw each plant
        for p in self.eco.plants:
            self.ctx.fillStyle = self.colors.get(p.species, "#FFF")
            self.ctx.fillRect(
                p.x * self.tile,
                p.y * self.tile,
                self.tile,
                self.tile
            )

# ————————————————————————————————————————————————————————————————————————————
# Bootstrapping
eco = Ecosystem()
rnd = Renderer("game", eco)

def tick(_=None):
    eco.update()
    rnd.render()

# Instead of importing create_proxy, just schedule directly:
from js import window

# window.setInterval will automatically wrap your Python function
window.setInterval(tick, 500)