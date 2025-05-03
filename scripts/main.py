from ecosystem import Ecosystem
from rendering import Renderer
from pyscript import loop

ecosystem = Ecosystem()
renderer = Renderer("game", ecosystem)

def update():
    ecosystem.update()
    renderer.render()

# Update ecosystem every 0.5 seconds
loop.schedule_interval(update, 0.5)
