from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivymd.uix.button import MDRectangleFlatButton, MDIconButton
from kivymd.uix.label import MDLabel

KV = f'''
Screen:
    ScrollView:
        id: scroll_view
        size_hint: (1, 1)  # Changed from (1, None)
        
        MDList:
            id: saved_list
            size_hint_y: None
            height: self.minimum_height
            md_bg_color: (1,1,1,1)
            padding: 0  # Set padding to 0
            spacing: 0 
            
            CustomListItem:
            CustomListItem:
            CustomListItem:
            CustomListItem:
            CustomListItem:
            CustomListItem:
            CustomListItem:
            CustomListItem:
            CustomListItem:
            CustomListItem:
            CustomListItem:
            CustomListItem:
            CustomListItem:
            CustomListItem:
            CustomListItem:
            CustomListItem:
            CustomListItem:
            CustomListItem:
            CustomListItem:
            CustomListItem:
            CustomListItem:
            CustomListItem:
            CustomListItem:
            CustomListItem:
            CustomListItem:

<CustomListItem@BoxLayout>:
    size_hint_y: None
    height: dp(48)  # Adjust the height as needed
    
    orientation: 'horizontal'
    spacing: '10dp'

    MDLabel:
        text: "Custom Item"
        halign: 'center'

    MDIconButton:
        icon: 'alpha-a'
        size_hint_x: None
        width: "100dp"
    MDIconButton:
        icon: 'alpha-b'
        size_hint_x: None
        width: "100dp"
    MDIconButton:
        icon: 'alpha-c'
        size_hint_x: None
        width: "100dp"
    MDIconButton:
        icon: 'alpha-d'
        size_hint_x: None
        width: "100dp"
'''

class TestApp(MDApp):
    def build(self):
        return Builder.load_string(KV)

TestApp().run()

