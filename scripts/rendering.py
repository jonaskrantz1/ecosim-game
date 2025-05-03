from js import document, Image

class Renderer:
    def __init__(self, canvas_id, ecosystem):
        can = document.getElementById(canvas_id)
        self.ctx = can.getContext("2d")
        self.eco = ecosystem
        self.tile = 16

        # 16×32 sprite sheet
        self.img = Image.new()
        self.img.src = "assets/sprites.png"

        self.sprite_y = {
            "Grass":    0,
            "Bush":     16
        }
        self.terrain_colors = {
            "water":     "#2060b4",
            "swamp":     "#445c3c",
            "sand":      "#e1c16e",
            "grassland": "#4CAF50",
            "hills":     "#888c6d",
            "mountains": "#777777"
        }

    def render(self):
        if not self.img.complete:
            return

        # draw terrain
        self.ctx.clearRect(0, 0, 64*self.tile, 48*self.tile)
        for y in range(48):
            for x in range(64):
                t = self.eco.terrain[y][x]
                self.ctx.fillStyle = self.terrain_colors[t]
                self.ctx.fillRect(x*self.tile, y*self.tile, self.tile, self.tile)

        # draw plants
        for p in self.eco.plants:
            yoff = self.sprite_y.get(p.species, 0)
            self.ctx.drawImage(
                self.img,
                0, yoff, self.tile, self.tile,
                p.x*self.tile, p.y*self.tile,
                self.tile, self.tile
            )
