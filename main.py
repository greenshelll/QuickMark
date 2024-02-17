from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup

class HelloWorldApp(App):
    def build(self):
        # Create a label widget
        label = Label(text="Hello, World!")

        # Create a button widget
        button = Button(text="Click me!")
        button.bind(on_press=self.show_popup)

        # Add the label and button to the layout
        layout = button
        layout.add_widget(label)

        return layout

    def show_popup(self, instance):
        # Create a popup message
        popup = Popup(title='Popup Message',
                      content=Label(text='You clicked the button!'),
                      size_hint=(None, None), size=(400, 200))

        # Display the popup
        popup.open()

if __name__ == '__main__':
    HelloWorldApp().run()
