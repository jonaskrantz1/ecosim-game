import json
import random
from pyodide.http import open_url
from js import document, window, Image, simplex
from pyodide.ffi import create_proxy

# ————————————————————————————————————————————————————————————————————————————
# Constants
GRID_WIDTH  = 64   # 1024 / 16
GRID_HEIGHT = 48   # 768 / 16
TILE_SIZE   = 16

# ————————————————————————————————————————————————————————————————————————————
# Helper: load JSON from your data folder
def load_json(path):
    resp = open_url(path)
    return json.loads(resp.read())

# ————————————————————————————————————————————————————————————————————————————
# Plant & Ecosystem
class Plant:
    def __init__(self, attrs, x, y):
        self.species = attrs["species"]
        self.x = x
        self.y = y
        self.age = 0
        self.attrs = attrs

class Ecosystem:
    def __init__(self):
        self.terrain = self.generate_terrain()
        data = load_json("data/plants.json")
        self.plants = [
            Plant(attrs, (i * 3) % GRID_WIDTH, (i * 5) % GRID_HEIGHT)
            for i, attrs in enumerate(data)
        ]
        self.occupied = {(p.x, p.y) for p in self.plants}

    def generate_terrain(self):
        """Generate smooth biomes using JS SimplexNoise."""
        scale  = 0.1
        offset = 100.0  # separate noise fields
        terrain = []
        for y in range(GRID_HEIGHT):
            row = []
            for x in range(GRID_WIDTH):
                e = simplex.noise2D(x * scale, y * scale)
                m = simplex.noise2D(x * scale + offset, y * scale + offset)
                if e < -0.05:
                    row.append("water")
                elif e < 0:
                    row.append("swamp" if m > 0 else "sand")
                elif e < 0.1:
                    row.append("grassland" if m > 0 else "sand")
                elif e < 0.25:
                    row.append("hills")
                else:
                    row.append("mountains")
            terrain.append(row)
        return terrain

    def update(self):
        new_plants = []
        if len(self.plants) > 1000:
            return

        for p in self.plants:
            p.age += 1
            if random.random() < p.attrs["reproduction_rate"]:
                dirs = [(-1,0),(1,0),(0,-1),(0,1)]
                random.shuffle(dirs)
                for dx, dy in dirs:
                    nx, ny = p.x + dx, p.y + dy
                    if (0 <= nx < GRID_WIDTH and
                        0 <= ny < GRID_HEIGHT and
                        (nx, ny) not in self.occupied):
                        new = Plant(p.attrs, nx, ny)
                        new_plants.append(new)
                        self.occupied.add((nx, ny))
                        break
        self.plants.extend(new_plants)

# ————————————————————————————————————————————————————————————————————————————
# Renderer
class Renderer:
    def __init__(self, canvas_id, ecosystem):
        can = document.getElementById(canvas_id)
        self.ctx = can.getContext("2d")
        self.eco = ecosystem
        self.tile = TILE_SIZE

        # load spritesheet
        self.img = Image.new()
        self.img.src = "assets/sprites.png"

        self.sprite_y = {
            "Grass": 0,
            "Bush":  16
        }
        self.terrain_colors = {
            "water":      "#2060b4",
            "swamp":      "#445c3c",
            "sand":       "#e1c16e",
            "grassland":  "#4CAF50",
            "hills":      "#888c6d",
            "mountains":  "#777777"
        }

    def render(self):
        if not self.img.complete:
            return

        # draw terrain base
        self.ctx.clearRect(0, 0,
            GRID_WIDTH * self.tile, GRID_HEIGHT * self.tile)
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                t = self.eco.terrain[y][x]
                self.ctx.fillStyle = self.terrain_colors[t]
                self.ctx.fillRect(
                    x * self.tile, y * self.tile,
                    self.tile, self.tile
                )

        # draw plants on top
        for p in self.eco.plants:
            y_off = self.sprite_y.get(p.species, 0)
            self.ctx.drawImage(
                self.img,
                0, y_off, self.tile, self.tile,
                p.x * self.tile, p.y * self.tile,
                self.tile, self.tile
            )

# ————————————————————————————————————————————————————————————————————————————
# Bootstrapping & Loop
eco = Ecosystem()
rnd = Renderer("game", eco)

def tick(_=None):
    eco.update()
    rnd.render()

proxy = create_proxy(tick)
window.setInterval(proxy, 500)
