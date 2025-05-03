from js import document

class Renderer:
    def __init__(self, canvas_id, ecosystem):
        canvas = document.getElementById(canvas_id)
        self.ctx = canvas.getContext('2d')
        self.ecosystem = ecosystem
        self.tile_size = 16
        self.colors = {
            'Grass': '#4CAF50',
            'Bush': '#8BC34A',
            'Tree': '#388E3C'
        }

    def render(self):
        self.ctx.clearRect(0, 0, 1024, 768)
        for plant in self.ecosystem.plants:
            color = self.colors.get(plant.species, '#FFFFFF')
            self.ctx.fillStyle = color
            self.ctx.fillRect(
                plant.x * self.tile_size,
                plant.y * self.tile_size,
                self.tile_size,
                self.tile_size
            )
