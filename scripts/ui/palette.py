from js import document

class Palette:
    def __init__(self, items, select_callback, item_type='icon'):
        self.items = items
        self.select_callback = select_callback
        self.item_type = item_type
        self.element = document.createElement('div')
        self.element.classList.add('palette')

    def render(self):
        self.element.innerHTML = ''
        document.body.appendChild(self.element)

        for item in self.items:
            elem = document.createElement('div' if self.item_type == 'color' else 'img')
            
            if self.item_type == 'color':
                elem.style.backgroundColor = item["color"]
                elem.classList.add('palette-color')
            else:
                elem.src = f'assets/icons/{item["species"].lower()}.png'
                elem.classList.add('palette-icon')
                
            elem.onclick = lambda evt, itm=item: self.select_item(itm)
            self.element.appendChild(elem)

    def select_item(self, item):
        self.select_callback(item)
        self.close()

    def close(self):
        if self.element.parentElement:
            self.element.parentElement.removeChild(self.element)
