import json
from pyodide.http import open_url
from js import document
import random

GRID_WIDTH = 64   # 1024 / 16
GRID_HEIGHT = 48  # 768 / 16


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
        self.occupied = set((p.x, p.y) for p in self.plants)


    

    def update(self):
        new_plants = []
        if len(self.plants) > 1000:
            return

        for p in self.plants:
            p.age += 1

            # Attempt to reproduce
            if random.random() < p.attrs["reproduction_rate"]:
                # Try 4 adjacent tiles (up/down/left/right)
                for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
                    nx, ny = p.x + dx, p.y + dy
                    if (0 <= nx < GRID_WIDTH and
                        0 <= ny < GRID_HEIGHT and
                        (nx, ny) not in self.occupied):

                        new_p = Plant(p.attrs, nx, ny)
                        new_plants.append(new_p)
                        self.occupied.add((nx, ny))
                        break  # only spread once
        self.plants.extend(new_plants)

# ————————————————————————————————————————————————————————————————————————————
# Renderer
from js import Image

class Renderer:
    def __init__(self, canvas_id, ecosystem):
        can = document.getElementById(canvas_id)
        self.ctx = can.getContext("2d")
        self.eco = ecosystem
        self.tile = 16

        # Sprite image
        self.img = Image.new()
        self.img.src = "assets/sprites.png"

        # Map species to sprite Y-offset (in pixels)
        self.sprite_y = {
            "Grass": 0,
            "Bush": 16
        }

    def render(self):
        self.ctx.clearRect(0, 0, 1024, 768)
        for p in self.eco.plants:
            y_offset = self.sprite_y.get(p.species, 0)
            self.ctx.drawImage(
                self.img,
                0, y_offset, 16, 16,                 # source (from sprite)
                p.x * self.tile, p.y * self.tile,    # destination position
                16, 16                               # destination size
            )


# ————————————————————————————————————————————————————————————————————————————
# Bootstrapping
eco = Ecosystem()
rnd = Renderer("game", eco)

def tick(_=None):
    eco.update()
    rnd.render()

# run every 500 ms using the browser's setInterval
from js import window
from pyodide.ffi import create_proxy

tick_proxy = create_proxy(tick)
window.setInterval(tick_proxy, 500)
