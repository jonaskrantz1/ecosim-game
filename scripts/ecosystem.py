from utils import load_json

class Plant:
    def __init__(self, species, x, y, attributes):
        self.species = species
        self.x = x
        self.y = y
        self.attributes = attributes
        self.age = 0

class Ecosystem:
    def __init__(self):
        plant_data = load_json('data/plants.json')
        # Spread plants evenly initially
        self.plants = [
            Plant(species=p['species'],
                  x=(i * 3) % 64,        # mod by grid width
                  y=(i * 5) % 48,        # mod by grid height
                  attributes=p)
            for i, p in enumerate(plant_data)
        ]

    def update(self):
        for plant in self.plants:
            plant.age += 1
