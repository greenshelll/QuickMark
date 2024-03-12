from kivy.lang.builder import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from datetime import datetime
from kivymd.uix.button import MDFlatButton,MDRaisedButton, MDRectangleFlatButton, MDRoundFlatButton, MDFillRoundFlatButton
from kivymd.uix.card import MDSeparator
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.stacklayout import MDStackLayout
from kivymd.uix.card import MDCard
from screens.camera import CameraWidget
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.core.window import Window
from kivymd.uix.list import MDList, OneLineListItem

Window.size= (288,640)

KV = '''
CustomScreenManager:
    HomeScreen:
    NameScreen:
    CheckScreen:
    MCScreen:

<HomeScreen>:
    name: 'home'

    MDStackLayout:
        MDTopAppBar:
            title: "QuickMark"
            right_action_items: [["plus-circle", lambda x: setattr(root.manager, 'current', 'name')]]
            elevation: 0

        ScrollView:
            MDList:
                id: saved_list
                 
<NameScreen>:
    name: 'name'

    MDLabel:
        id: display_label
        text: ""
        halign: "center"
        pos_hint: {"top": 1.33}
        

    MDTopAppBar:
        title: "QuickMark"
        pos_hint: {"top": 1}
        elevation: 0

    MDTextField:
        id: text_field
        mode: "rectangle"
        size_hint_x: None
        width: "240dp"
        pos_hint: {"top":.879, "center_x": .5}
        hint_text: "Name of test"
        on_text_validate: app.update_label(self); root.add_item_to_list(self.text)
    
    MDFloatLayout:
        MDRaisedButton:
            id: save_button
            text: "SAVE"
            pos_hint:{"top":.85, "center_x": .7}
            on_press: app.save_and_display_text()
            elevation: 0

    MDSeparator:
        pos_hint: {"top": .75}
        size_hint_y: None
        height: dp(1)

    MDLabel:
        text:"Appraisal"
        halign: "center"
        pos_hint: {"center_y":.73}
    
    MDRectangleFlatButton:
        text: "CHECK SHEETS" 
        pos_hint: {"top":.68, "center_x": .5}
        on_press: root.manager.current = 'check'
          

    MDRectangleFlatButton:
        text: "ANALYSIS"
        pos_hint: {"top":.61, "center_x": .5}
              

    MDSeparator:
        pos_hint: {"top":.5, "center_x": .5}
        size_hint_y: None
        height: dp(1)  

    MDLabel:
        text:"Generate Answer Sheet"
        halign: "center"
        pos_hint: {"center_y":.48}

    MDRectangleFlatButton:
        text: "GENERATE"
        pos_hint: {"top":.43, "center_x": .5}

    MDSeparator:
        pos_hint: {"top":.32, "center_x": .5}
        size_hint_y: None
        height: dp(1)

    MDLabel:
        text:"Edit Answer Key"
        halign: "center"
        pos_hint: {"center_y":.3}

    MDRectangleFlatButton:
        text: "MULTIPLE CHOICE"
        pos_hint: {"top":.24, "center_x": .5}
        on_press: root.manager.current = 'MC'

    MDRectangleFlatButton:
        text: "TRUE OR FALSE"
        pos_hint: {"top":.17, "center_x": .5}

    MDRectangleFlatButton:
        text: "IDENTIFICATION"
        pos_hint: {"top":.1, "center_x": .5}

    MDIconButton:
        id: back_button
        icon: "arrow-left"
        pos_hint: {"top":.07, "center_x": .5}
        on_press: root.manager.current = 'home'
            


<CheckScreen>:
    name: 'check'
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1  # White color
        Rectangle:
            size: self.size
            pos: self.pos

    MDTopAppBar:
        title: "QuickMark"
        elevation: 0
        pos_hint: {"top": 1}

    MDIconButton:
        id: camera_icon
        icon: "camera-outline"
        pos_hint: {"top":.2, "center_x": .5}
        on_release: root.switch_cam()

    MDIconButton:
        id: back_button
        icon: "arrow-left"
        pos_hint: {"top":.07, "center_x": .5}
        on_press: root.manager.current = 'name'


<MCScreen>:
    name: 'MC'

    MDBoxLayout:
        orientation: 'vertical'
        adaptive_height: True
        pos_hint: {'top': 1}  # Align to the top

        MDTopAppBar:
            title: "QuickMark"
            right_action_items: [["plus-circle", lambda x: setattr(root.manager, 'current', 'name')]]
            elevation: 0
            
        MDBoxLayout:
            orientation: 'horizontal'
            spacing: dp(10)
            size_hint_y: None
            height: self.minimum_height

            MDLabel:
                text: '1.'
            
            MDRoundFlatButton:
                text:'A'
                size_hint: None, None
                width: root.width*0.2
                height: root.height*0.04

            MDRoundFlatButton:
                text:'B'
                size_hint: None, None
                width: root.width*0.2
                height: root.height*0.04

            MDRoundFlatButton:
                text:'C'
                size_hint: None, None
                width: root.width*0.2
                height: root.height*0.04

            MDRoundFlatButton:
                text:'D'
                size_hint: None, None
                width: root.width*0.2
                height: root.height*0.04


'''


class CustomScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.transition = NoTransition()
        

class HomeScreen(Screen):
    def add_item_to_list(self, item_text):
        saved_list = self.ids.saved_list
        saved_list.add_widget(OneLineListItem(text=item_text))


class NameScreen(Screen):
    def add_item_to_list(self, text):
        home_screen = self.manager.get_screen('home')
        saved_list = home_screen.ids.saved_list
        saved_list.add_widget(OneLineListItem(text=text))



class CheckScreen(Screen):
    def switch_cam(self,*args,**kwargs):
        if self.cam_is_on == False:
            self.camera_widget = CameraWidget()
            self.add_widget(self.camera_widget)
            self.cam_is_on = True
        else:
            self.remove_widget(self.camera_widget)
            self.camera_widget.remove_camera = True
            self.camera_widget.camera.remove_from_cache()
            self.camera_widget.camera.play = False
            del self.camera_widget.camera._camera
            del self.camera_widget
            self.cam_is_on = False
            

    def __init__(self,**kwargs):
        super(CheckScreen, self).__init__(**kwargs)
        self.cam_is_on = False

class MCScreen(Screen):
    pass

        

class App(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Purple"
        screen = Builder.load_string(KV)
        return screen
    
    def update_label(self, instance):
        text_input = instance.text
        display_label = self.root.get_screen('name').ids.display_label
        current_date = datetime.now().strftime('%Y-%m-%d')
        display_label.text = f"{text_input}\n{current_date}"
        text_field = self.root.get_screen('name').ids.text_field
        self.root.get_screen('name').remove_widget(text_field)
        save_button = self.root.get_screen('name').ids.save_button
        self.root.get_screen('name').remove_widget(save_button.parent)

    def save_and_display_text(self):
        text_input = self.root.get_screen('name').ids.text_field.text
        self.update_label(self.root.get_screen('name').ids.text_field)

        # Add item to the list
        home_screen = self.root.get_screen('home')
        home_screen.add_item_to_list(text_input)

        # Remove save button
        save_button = self.root.get_screen('name').ids.save_button
        self.root.get_screen('name').remove_widget(save_button.parent)


App().run()