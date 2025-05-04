from pyodide.http import open_url
from pyodide.ffi import create_proxy
from js import window, document

# Dynamically load existing modules
def _load_and_exec(path):
    src = open_url(path).read()
    exec(src, globals())

for mod in ("utils.py", "ecosystem.py", "rendering.py"):
    _load_and_exec(f"scripts/{mod}")

# Dynamically load UI modules (ensure these files exist!)
for mod in ("ui/button.py", "ui/toolbar.py", "ui/palette.py"):
    _load_and_exec(f"scripts/{mod}")

# Initialize ecosystem and renderer
eco = Ecosystem()
rnd = Renderer("game", eco)

# Initialize Toolbar UI
toolbar = Toolbar()
toolbar.render()


def canvas_click(evt):
    tile_size = rnd.tile
    canvas = evt.target
    rect = canvas.getBoundingClientRect()
    x = int((evt.clientX - rect.left) / tile_size)
    y = int((evt.clientY - rect.top) / tile_size)

    if hasattr(window, 'current_selected_plant') and window.current_selected_plant:
        plant_attrs = window.current_selected_plant
        if (x, y) not in eco.occupied:
            new_plant = Plant(plant_attrs, x, y)
            eco.plants.append(new_plant)
            eco.occupied.add((x, y))
            print(f'Planted {plant_attrs["species"]} at ({x}, {y})')

    elif hasattr(window, 'current_selected_terrain') and window.current_selected_terrain:
        eco.terrain[y][x] = window.current_selected_terrain
        print(f'Set terrain to {window.current_selected_terrain} at ({x}, {y})')

canvas_elem = document.getElementById('game')
canvas_elem.addEventListener('click', create_proxy(canvas_click))


# Main update loop
def tick(_=None):
    eco.update()
    rnd.render()

proxy = create_proxy(tick)
window.setInterval(proxy, 500)
