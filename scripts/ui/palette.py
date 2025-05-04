from js import document

class Palette:
    def __init__(self, items, select_callback):
        self.items = items
        self.select_callback = select_callback
        self.element = document.createElement('div')
        self.element.classList.add('palette')

    def render(self):
        self.element.innerHTML = ''  # clear existing
        document.body.appendChild(self.element)

        for item in self.items:
            icon = document.createElement('img')
            icon.src = f'assets/icons/{item["species"].lower()}.png'
            icon.classList.add('palette-icon')
            icon.onclick = lambda evt, itm=item: self.select_item(itm)
            self.element.appendChild(icon)

    def select_item(self, item):
        self.select_callback(item)
        self.close()

    def close(self):
        if self.element.parentElement:
            self.element.parentElement.removeChild(self.element)
