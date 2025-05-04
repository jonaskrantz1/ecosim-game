from js import document

class Button:
    def __init__(self, icon_path, action):
        self.icon_path = icon_path
        self.action = action
        self.element = document.createElement('img')
        self.element.src = icon_path
        self.element.classList.add('ui-button')
        self.element.onclick = self.on_click

    def render(self, parent):
        parent.appendChild(self.element)

    def on_click(self, event):
        self.action()
