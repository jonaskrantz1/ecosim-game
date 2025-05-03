import json
import random
import math
from pyodide.http import open_url
from js import document, window, Image
from pyodide.ffi import create_proxy

# ————————————————————————————————————————————————————————————————————————————
# Constants
GRID_WIDTH  = 64
GRID_HEIGHT = 48
TILE_SIZE   = 16

# ————————————————————————————————————————————————————————————————————————————
# PURE-PYTHON PERLIN NOISE
_perm = list(range(256))
random.shuffle(_perm)
_perm += _perm

def _fade(t):
    return t * t * t * (t * (t * 6 - 15) + 10)

def _lerp(a, b, t):
    return a + t * (b - a)

def _grad(hash, x, y):
    h = hash & 3
    u = x if h < 2 else y
    v = y if h < 2 else x
    return (u if (h & 1) == 0 else -u) + (v if (h & 2) == 0 else -v)

def perlin(x, y):
    xi = int(math.floor(x)) & 255
    yi = int(math.floor(y)) & 255
    xf = x - math.floor(x)
    yf = y - math.floor(y)
    u = _fade(xf)
    v = _fade(yf)

    aa = _perm[_perm[xi] + yi]
    ab = _perm[_perm[xi] + yi + 1]
    ba = _perm[_perm[xi + 1] + yi]
    bb = _perm[_perm[xi + 1] + yi + 1]

    x1 = _lerp(_grad(aa, xf, yf), _grad(ba, xf - 1, yf), u)
    x2 = _lerp(_grad(ab, xf, yf - 1), _grad(bb, xf - 1, yf - 1), u)
    return _lerp(x1, x2, v)

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
        self.occupied = {(p.x, p.y) for p in self.plants}

    def generate_terrain(self):
        """Generate terrain with fixed distribution percentages."""
        scale = 0.1
        terrain = []
        for y in range(GRID_HEIGHT):
            row = []
            for x in range(GRID_WIDTH):
                e = perlin(x * scale, y * scale)   # in [-1,1]
                norm = (e + 1) / 2                # now in [0,1]

                if   norm < 0.20:  biome = "water"
                elif norm < 0.30:  biome = "swamp"
                elif norm < 0.70:  biome = "grassland"
                elif norm < 0.90:  biome = "hills"
                else:              biome = "mountains"

                row.append(biome)
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
                for dx,dy in dirs:
                    nx,ny = p.x+dx, p.y+dy
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

        self.img = Image.new()
        self.img.src = "assets/sprites.png"

        self.sprite_y = {
            "Grass":    0,
            "Bush":     16
        }
        self.terrain_colors = {
            "water":    "#2060b4",
            "swamp":    "#445c3c",
            "sand":     "#e1c16e",
            "grassland":"#4CAF50",
            "hills":    "#888c6d",
            "mountains":"#777777"
        }

    def render(self):
        if not self.img.complete:
            return

        self.ctx.clearRect(0, 0, GRID_WIDTH * self.tile, GRID_HEIGHT * self.tile)

        # draw terrain
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                t = self.eco.terrain[y][x]
                self.ctx.fillStyle = self.terrain_colors[t]
                self.ctx.fillRect(x * self.tile, y * self.tile, self.tile, self.tile)

        # draw plants
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
