from ecosystem import Ecosystem
from rendering import Renderer
from utils import load_json
from pyscript import loop

ecosystem = Ecosystem()
renderer = Renderer("game", ecosystem)

def update():
    ecosystem.update()
    renderer.render()

loop.schedule_interval(update, 0.5)

