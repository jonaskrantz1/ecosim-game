from js import document

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
        terrain_colors = [
            {"type": "water", "color": "#2060b4"},
            {"type": "swamp", "color": "#445c3c"},
            {"type": "sand", "color": "#e1c16e"},
            {"type": "grassland", "color": "#4CAF50"},
            {"type": "hills", "color": "#888c6d"},
            {"type": "mountains", "color": "#777777"}
        ]
        palette = Palette(terrain_colors, self.select_terrain, item_type='color')
        palette.render()

    def select_terrain(self, terrain):
        window.current_selected_terrain = terrain["type"]
        window.current_selected_plant = None  # deselect plant
        print(f'Selected terrain: {terrain["type"]}')

    def open_plant_palette(self):
        plant_data = load_json("data/plants.json")
        palette = Palette(plant_data, self.select_plant)
        palette.render()

    def select_plant(self, plant_attrs):
        window.current_selected_plant = plant_attrs
        window.current_selected_terrain = None  # deselect terrain
        print(f'Selected plant: {plant_attrs["species"]}')

    def open_animal_palette(self):
        print("Open Animal Palette")

    def open_object_palette(self):
        print("Open Object Palette")

    def activate_remove_mode(self):
        window.current_selected_plant = None
        window.current_selected_terrain = None
        print("Remove Mode Active")
