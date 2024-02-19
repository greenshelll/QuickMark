import toga
from toga.style import Pack

def update_style(parent, widget, style):
    parent.remove(widget)
    widget = toga.Button(widget.text, on_press=widget.on_press, style=style)
    parent.add(widget)
    return (parent, widget)

def get_propsize(base_size, width_prop, height_prop):
    size = base_size
    return (int(size[0] * width_prop), int(size[1] * height_prop))