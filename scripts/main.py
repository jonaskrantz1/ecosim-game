from scripts.ecosystem import Ecosystem
from scripts.rendering import Renderer
from scripts.utils import *
from pyscript import loop


ecosystem = Ecosystem()
renderer = Renderer("game", ecosystem)

def update():
    ecosystem.update()
    renderer.render()

# Update ecosystem every 0.5 seconds
loop.schedule_interval(update, 0.5)
