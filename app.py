from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from screens.camera import CameraWidget
from kivy.graphics import Color, Rectangle
from kivy.utils import get_color_from_hex
from kivy.core.window import Window
class MainApp(App):
    def build(self):
        layout = FloatLayout(size_hint=(1, 1))  # Set size hint to fill all available space

        # Set background color to white
        with layout.canvas.before:
            Color(*get_color_from_hex("#FFFFFF"))
            self.rect = Rectangle(size=layout.size, pos=layout.pos)

        camera_widget = CameraWidget()
        layout.add_widget(camera_widget)
        layout.bind(size=self._update_rect, pos=self._update_rect)  # Bind rectangle to layout size and position
        return layout

    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

    def on_start(self):
        # Get window size
        window_width, window_height = Window.size
        print("Window size:", window_width, window_height)


if __name__ == '__main__':
    MainApp().run() 
    