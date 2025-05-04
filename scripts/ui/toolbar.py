from js import document
from .button import Button

class Toolbar:
    def __init__(self):
        self.element = document.createElement('div')
        self.element.classList.add('toolbar')

        self.buttons = [
            Button('assets/icons/terrain.png', self.open_terrain_palette),
            Button('assets/icons/plant.png', self.open_plant_palette),
            Button('assets/icons/animal.png', self.open_animal_palette),
            Button('assets/icons/object.png', self.open_object_palette),
            Button('assets/icons/remove.png', self.activate_remove_mode),
        ]

    def render(self):
        document.body.appendChild(self.element)
        for btn in self.buttons:
            btn.render(self.element)

    def open_terrain_palette(self):
        print("Open Terrain Palette")

    def open_plant_palette(self):
        print("Open Plant Palette")

    def open_animal_palette(self):
        print("Open Animal Palette")

    def open_object_palette(self):
        print("Open Object Palette")

    def activate_remove_mode(self):
        print("Remove Mode Active")
