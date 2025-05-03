from js import document

class Renderer:
    def __init__(self, canvas_id, ecosystem):
        canvas = document.getElementById(canvas_id)
        self.ctx = canvas.getContext('2d')
        self.ecosystem = ecosystem
        self.tile_size = 8

    def render(self):
        self.ctx.clearRect(0, 0, 320, 200)
        # Later, logic for drawing plants goes here
