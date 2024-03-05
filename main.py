from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from screens.cam2 import CameraWidget

class MainApp(App):
    def build(self):
        layout = FloatLayout()
        camera_widget = CameraWidget()
        layout.add_widget(camera_widget)
        return layout

if __name__ == '__main__':
    MainApp().run() 
    