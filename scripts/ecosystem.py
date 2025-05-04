import random
from js import window

SUITABILITY = {
    "Grass": {
        "water":     0.0,
        "swamp":     0.5,
        "sand":      0.1,
        "grassland": 1.0,
        "hills":     0.8,
        "mountains": 0.2
    },
    "Bush": {
        "water":     0.0,
        "swamp":     0.7,
        "sand":      0.3,
        "grassland": 0.8,
        "hills":     1.0,
        "mountains": 0.5
    }
}

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
            Plant(attrs, (i * 3) % 64, (i * 5) % 48)
            for i, attrs in enumerate(data)
        ]
        self.occupied = {(p.x, p.y) for p in self.plants}
        self.tick_count = 0  # Track elapsed ticks (updates)

    def generate_terrain(self):
        terrain = []
        for y in range(48):
            row = []
            for x in range(64):
                e = perlin(x * 0.1, y * 0.1)
                norm = (e + 1) / 2

                if norm < 0.20:
                    row.append("water")
                elif norm < 0.30:
                    row.append("swamp")
                elif norm < 0.70:
                    row.append("grassland")
                elif norm < 0.90:
                    row.append("hills")
                else:
                    row.append("mountains")
            terrain.append(row)
        return terrain

    def update(self):
        self.tick_count += 1

        # Aging and survival check each tick
        survivors = []
        for p in self.plants:
            p.age += 1
            biome = self.terrain[p.y][p.x]
            factor = SUITABILITY[p.species].get(biome, 0.0)
            if factor > 0.0:
                survivors.append(p)

        self.plants = survivors
        self.occupied = {(p.x, p.y) for p in self.plants}

        # Reproduce only every 5 seconds (assuming update tick = 500ms, every 10 ticks)
        if self.tick_count % 10 == 0:
            self.reproduce()

    def reproduce(self):
        new_plants = []

        for p in self.plants:
            biome = self.terrain[p.y][p.x]
            factor = SUITABILITY[p.species].get(biome, 0.0)
            rate = p.attrs["reproduction_rate"] * factor
            if random.random() < rate:
                for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
                    nx, ny = p.x + dx, p.y + dy
                    if 0 <= nx < 64 and 0 <= ny < 48 and (nx, ny) not in self.occupied:
                        new_plants.append(Plant(p.attrs, nx, ny))
                        self.occupied.add((nx, ny))
                        break

        self.plants.extend(new_plants)
