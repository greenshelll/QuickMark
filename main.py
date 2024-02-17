from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.label import MDLabel


class CenteredLabelApp(MDApp):
    def build(self):
        layout = BoxLayout(orientation="vertical")
        label = MDLabel(text="Hello, KivyMD!", halign="center", valign="middle", font_style="H4")
        layout.add_widget(label)
        return layout


if __name__ == "__main__":
    CenteredLabelApp().run()
