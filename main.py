import json
import random
from pyodide.http import open_url
from js import document, window, Image
from pyodide.ffi import create_proxy

# ————————————————————————————————————————————————————————————————————————————
# Constants
GRID_WIDTH = 64   # 1024 / 16
GRID_HEIGHT = 48  # 768 / 16
TILE_SIZE = 16

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
        self.terrain = self.generate_terrain()
        data = load_json("data/plants.json")

        self.plants = [
            Plant(attrs, (i * 3) % GRID_WIDTH, (i * 5) % GRID_HEIGHT)
            for i, attrs in enumerate(data)
        ]
        self.occupied = set((p.x, p.y) for p in self.plants)

    def generate_terrain(self):
        coarse_w, coarse_h = 16, 12  # 64x48 divided into 4x4 chunks
        cell_w, cell_h = GRID_WIDTH // coarse_w, GRID_HEIGHT // coarse_h

        biotopes = ["water", "swamp", "sand", "grassland", "hills", "mountains"]

        # Create coarse biome map
        coarse = [
            [random.choice(biotopes) for _ in range(coarse_w)]
            for _ in range(coarse_h)
        ]

        # Expand to fine terrain
        terrain = []
        for y in range(GRID_HEIGHT):
            row = []
            for x in range(GRID_WIDTH):
                cx = x // cell_w
                cy = y // cell_h
                row.append(coarse[cy][cx])
            terrain.append(row)

        return terrain


    def update(self):
        new_plants = []
        if len(self.plants) > 1000:
            return

        for p in self.plants:
            p.age += 1

            # Attempt to reproduce
            if random.random() < p.attrs["reproduction_rate"]:
                dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
                random.shuffle(dirs)
                for dx, dy in dirs:
                    nx, ny = p.x + dx, p.y + dy
                    if (0 <= nx < GRID_WIDTH and
                        0 <= ny < GRID_HEIGHT and
                        (nx, ny) not in self.occupied):

                        new_p = Plant(p.attrs, nx, ny)
                        new_plants.append(new_p)
                        self.occupied.add((nx, ny))
                        break  # spread once only

        self.plants.extend(new_plants)

# ————————————————————————————————————————————————————————————————————————————
# Renderer
class Renderer:
    def __init__(self, canvas_id, ecosystem):
        can = document.getElementById(canvas_id)
        self.ctx = can.getContext("2d")
        self.eco = ecosystem
        self.tile = TILE_SIZE

        # Load sprite sheet
        self.img = Image.new()
        self.img.src = "assets/sprites.png"

        # Sprite mapping
        self.sprite_y = {
            "Grass": 0,
            "Bush": 16
        }

        # Terrain colors
        self.terrain_colors = {
            "water": "#2060b4",
            "swamp": "#445c3c",
            "sand": "#e1c16e",
            "grassland": "#4CAF50",
            "hills": "#888c6d",
            "mountains": "#777777"
        }

    def render(self):
        if not self.img.complete:
            return

        self.ctx.clearRect(0, 0, GRID_WIDTH * self.tile, GRID_HEIGHT * self.tile)

        # Draw terrain base
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                t = self.eco.terrain[y][x]
                self.ctx.fillStyle = self.terrain_colors.get(t, "#000")
                self.ctx.fillRect(x * self.tile, y * self.tile, self.tile, self.tile)

        # Draw plants
        for p in self.eco.plants:
            y_offset = self.sprite_y.get(p.species, 0)
            self.ctx.drawImage(
                self.img,
                0, y_offset, self.tile, self.tile,
                p.x * self.tile, p.y * self.tile,
                self.tile, self.tile
            )

# ————————————————————————————————————————————————————————————————————————————
# Bootstrapping
eco = Ecosystem()
rnd = Renderer("game", eco)

def tick(_=None):
    eco.update()
    rnd.render()

tick_proxy = create_proxy(tick)
window.setInterval(tick_proxy, 500)
