from kivy.lang.builder import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from datetime import datetime
from kivymd.uix.button import MDFlatButton,MDRaisedButton, MDRectangleFlatButton, MDRoundFlatButton, MDFillRoundFlatButton
from kivymd.uix.card import MDSeparator
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.stacklayout import MDStackLayout
from kivymd.uix.card import MDCard
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.core.window import Window
from kivymd.uix.list import MDList, OneLineListItem
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivy.properties import NumericProperty
#dinugang
from kivymd.uix.toolbar import MDTopAppBar, toolbar
from kivy.properties import StringProperty 
import os

Window.size= (288,640)
#Nagdugang ko OneCheckScreen kag ScoreScreen

KV = '''
CustomScreenManager:
    HomeScreen:
    NameScreen:
    OneCheckScreen:
    CheckScreen:
    ScoreScreen:
    MCScreen:
    TFScreen:
    IDScreen:
    AnalysisScreen:
    
    

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
        width: dp(280)
        _min_width: 200
        on_press: root.manager.current = 'onecheck'
          

    MDRectangleFlatButton:
        text: "ANALYSIS"
        pos_hint: {"top":.61, "center_x": .5}
        _min_width: 200
        on_press: root.manager.current = 'analysis'

              

    MDSeparator:
        pos_hint: {"top":.5, "center_x": .5}
        size_hint_y: None
        height: dp(1)  

    MDLabel:
        text:"Answer Sheet"
        halign: "center"
        pos_hint: {"center_y":.48}

    MDRectangleFlatButton:
        text: "EDIT SHEET"
        pos_hint: {"top":.43, "center_x": .5}
        _min_width: 200

    MDSeparator:
        pos_hint: {"top":.32, "center_x": .5}
        size_hint_y: None
        height: dp(1)

    MDLabel:
        text:"Answer Key"
        halign: "center"
        pos_hint: {"center_y":.3}

    MDRectangleFlatButton:
        text: "MULTIPLE CHOICE"
        pos_hint: {"top":.24, "center_x": .5}
        on_press: root.manager.current = 'MC'
        _min_width: 200

    MDRectangleFlatButton:
        text: "TRUE OR FALSE"
        pos_hint: {"top":.17, "center_x": .5}
        on_press: root.manager.current = 'TF'
        _min_width: 200


    MDRectangleFlatButton:
        text: "IDENTIFICATION"
        pos_hint: {"top":.1, "center_x": .5}
        on_press: root.manager.current = 'ID'
        _min_width: 200


    MDIconButton:
        id: back_button
        icon: "arrow-left"
        pos_hint: {"top":.07, "center_x": .5}
        on_press: root.manager.current = 'home'

<OneCheckScreen>
    name: 'onecheck'

    MDBoxLayout:
        orientation: 'vertical'

        MDStackLayout:
            MDTopAppBar:
                title: "QuickMark"
                right_action_items: [["plus-circle", lambda x: setattr(root.manager, 'current', 'name')]]
                elevation: 0

            ScrollView:
                MDList:
                    id: check_list
        
    MDRaisedButton:
        text: 'CHECK TEST'
        on_release: root.manager.current = 'check'
        pos_hint: {"top":.2, "center_x": .5}

    MDRaisedButton:
        text: "Add Item to List"
        pos_hint: {"top": .1, "center_x": .5}
        on_release: root.add_item_to_list()

<CheckScreen>:
    name: 'check'

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

<ScoreScreen>:
    name: 'score'

    MDTopAppBar:
        title: "QuickMark"
        elevation: 0
        pos_hint: {"top": 1}

    MDLabel:
        id: mc_label
        text: 'Multiple Choice'
        halign: 'center'
        pos_hint: {'top': 1.35}

    MDLabel:
        id: mc_score_label
        text: root.mc_score
        halign: 'center'
        pos_hint: {'top': 1.3}

    MDLabel:
        id: tf_label
        text: 'True or False'
        pos_hint: {'top': 1.25}
        halign: 'center'

    MDLabel:
        id: tf_score_label
        text: root.tf_score
        pos_hint: {'top': 1.2}
        halign: 'center'

    MDLabel:
        id: id_label
        text: 'Identification'
        pos_hint: {'top': 1.15}
        halign: 'center'

    MDLabel:
        id: id_score_label
        text: root.id_score
        pos_hint: {'top': 1.1}
        halign: 'center'

    MDSeparator:
        pos_hint: {"top":.5, "center_x": .5}
        size_hint_y: None
        height: dp(1)

    MDTextField:
        id: mc_score_input
        hint_text: "Enter score for Multiple Choice"
        on_text_validate: root.on_mc_score_entered()
        pos_hint: {"top": 0.45, "center_x": 0.5}

    MDTextField:
        id: tf_score_input
        hint_text: "Enter score for True or False"
        on_text_validate: root.on_tf_score_entered()
        pos_hint: {"top": 0.35, "center_x": 0.5}

    MDTextField:
        id: id_score_input
        hint_text: "Enter score for Identification"
        on_text_validate: root.on_id_score_entered()
        pos_hint: {"top": 0.25, "center_x": 0.5}





<AnalysisScreen>:
    name: 'analysis'

    MDBoxLayout:
        orientation: 'vertical'
        adaptive_height: True
        pos_hint: {'top': 1}  # Align to the top
        spacing: dp(10)

        MDTopAppBar:
            title: "QuickMark"
            right_action_items: [["cog-outline", lambda x: app.show_text_input_dialog()]]
            elevation: 0
        
        MDLabel:
            text: '#                          Percent'

            
        MDBoxLayout:
            orientation: 'horizontal'
            adaptive_height: True
            spacing: dp(5)

            MDLabel:
                text: '1.'

            Widget:
                id: graph_widget
                size_hint_x: None
                width: dp(50)
                canvas.before:
                    Color:
                        rgba: (0, 1, 0, 1) if root.percentage >= 0.75 else (1, 1, 0, 1) if 0.5 < root.percentage < 0.75 else (1, 0, 0, 1)  # Adjust color dynamically based on percentage
                    Rectangle:
                        pos: self.pos
                        size: self.width, root.percentage * self.height  # Adjust height dynamically based on percentage

            MDLabel:
                id: percentage_label
                text: f'{int(root.percentage * 100)}%'  # Display percentage dynamically

        MDTextField:
            hint_text: "Enter Percentage"
            helper_text: "Enter a value between 0 and 100"
            helper_text_mode: "persistent"
            input_filter: "float"
            multiline: False
            on_text_validate: root.update_percentage(self.text)


                
<MCScreen>:
    name: 'MC'

    MDBoxLayout:
        orientation: 'vertical'
        adaptive_height: True
        pos_hint: {'top': 1}  # Align to the top
        spacing: dp(10)

        MDTopAppBar:
            title: "QuickMark"
            right_action_items: [["cog-outline", lambda x: app.show_text_input_dialog()]]
            elevation: 0
            
        MDBoxLayout:
            orientation: 'horizontal'
            spacing: dp(10)
            size_hint_y: None
            height: self.minimum_height
            adaptive_width: True 
            id: mc_buttons  # Added an ID for accessing child buttons
            
            MDLabel:
                text: '1.'
                adaptive_width: True 

            
            MDRoundFlatButton:
                text:'A'
                size_hint: None, None
                width: root.width*0.1
                height: root.height*0.04
                on_release: root.toggle_button_state(self)  # Toggle button state
                md_bg_color: 1, 1, 1, 1  # Initial background color is white

            MDRoundFlatButton:
                text:'B'
                size_hint: None, None
                width: root.width*0.1
                height: root.height*0.04
                on_release: root.toggle_button_state(self)  # Toggle button state
                md_bg_color: 1, 1, 1, 1  # Initial background color is white

            MDRoundFlatButton:
                text:'C'
                size_hint: None, None
                width: root.width*0.1
                height: root.height*0.04
                on_release: root.toggle_button_state(self)  # Toggle button state
                md_bg_color: 1, 1, 1, 1  # Initial background color is white

            MDRoundFlatButton:
                text:'D'
                size_hint: None, None
                width: root.width*0.1
                height: root.height*0.04
                on_release: root.toggle_button_state(self)  # Toggle button state
                md_bg_color: 1, 1, 1, 1  # Initial background color is white


<TFScreen>:
    name: 'TF'

    MDBoxLayout:
        orientation: 'vertical'
        adaptive_height: True
        pos_hint: {'top': 1}  # Align to the top
        spacing: dp(10)

        MDTopAppBar:
            title: "QuickMark"
            right_action_items: [["cog-outline", lambda x: app.show_text_input_dialog()]]  # Use the same button as in MCScreen
            elevation: 0
            
        MDBoxLayout:
            id: tf_buttons  # Add id to the MDBoxLayout containing buttons
            orientation: 'horizontal'
            spacing: dp(10)
            size_hint_y: None
            height: self.minimum_height
            adaptive_width: True 
        
            MDLabel:
                text: '1.'
                adaptive_width: True 

            
            MDRoundFlatButton:
                text:'T'
                size_hint: None, None
                width: root.width*0.1
                height: root.height*0.04
                on_release: root.toggle_button_state(self)  # Toggle button state

            MDRoundFlatButton:
                text:'F'
                size_hint: None, None
                width: root.width*0.1
                height: root.height*0.04
                on_release: root.toggle_button_state(self)  # Toggle button state



<IDScreen>:
    name: 'ID'

    MDBoxLayout:
        orientation: 'vertical'
        adaptive_height: True
        pos_hint: {'top': 1}  # Align to the top
        spacing: dp(10)

        MDTopAppBar:
            title: "QuickMark"
            right_action_items: [["cog-outline", lambda x: setattr(root.manager, 'current', 'name')]]
            elevation: 0

        MDBoxLayout:
            orientation: 'horizontal'
            spacing: dp(10)
            size_hint_y: None
            height: self.minimum_height
            adaptive_width: True 
        
            MDLabel:
                text: '1.'
                adaptive_width: True 
            
            MDTextField:
                mode: "rectangle"
                size_hint: None, None
                width: "240dp" 
                font_size:'18dp'
                max_text_length: 15
  

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

#ari dinugang man
class OneCheckScreen(Screen):
    def add_item_to_list(self, item_text="New Item Added"):
        check_list = self.ids.check_list
        list_item = OneLineListItem(text=item_text)
        list_item.bind(on_release=self.go_to_score_screen)
        check_list.add_widget(list_item)

    def go_to_score_screen(self, instance):
        self.manager.current = 'score'



class CheckScreen(Screen):
    pass

#kag ari
class ScoreScreen(Screen):
    mc_score = StringProperty('')
    tf_score = StringProperty('')
    id_score = StringProperty('')

    def on_mc_score_entered(self):
        self.mc_score = self.ids.mc_score_input.text

    def on_tf_score_entered(self):
        self.tf_score = self.ids.tf_score_input.text

    def on_id_score_entered(self):
        self.id_score = self.ids.id_score_input.text
        
class AnalysisScreen(Screen):
    percentage = NumericProperty(0.5)  # Example percentage value

    def update_percentage(self, value):
        try:
            percentage = float(value) / 100
            if 0 <= percentage <= 1:
                self.percentage = percentage
            else:
                print("Percentage must be between 0 and 100.")
        except ValueError:
            print("Invalid input. Please enter a valid percentage.")

class MCScreen(Screen):
    def toggle_button_state(self, button):
        # Deselect all buttons
        buttons = self.ids.mc_buttons.children
        for btn in buttons:
            if btn != button:
                btn.md_bg_color = [1, 1, 1, 1]  # Revert background color to white
        
        # Highlight the pressed button
        if button.md_bg_color == [1, 1, 1, 1]:  # If the background color is white
            button.md_bg_color = [.5, .5, .5, 1]  # Change it to the desired color
        else:
            button.md_bg_color = [1, 1, 1, 1]  # Revert to white

    def on_pre_enter(self, *args):
        # Reset button background color when screen is entered
        buttons = self.ids.mc_buttons.children
        for button in buttons:
            button.md_bg_color = [1, 1, 1, 1]  # Set all buttons to white initially

    def on_leave(self, *args):
        # Reset button background color when leaving the screen
        self.on_pre_enter()



class TFScreen(Screen):
    def toggle_button_state(self, button):
        # Deselect all buttons
        buttons = self.ids.tf_buttons.children
        for btn in buttons:
            if btn != button:
                btn.md_bg_color = [1, 1, 1, 1]  # Revert background color to white
        
        # Highlight the pressed button
        if button.md_bg_color == [1, 1, 1, 1]:  # If the background color is white
            button.md_bg_color = [.5, .5, .5, 1]  # Change it to the desired color
        else:
            button.md_bg_color = [1, 1, 1, 1]  # Revert to white

    def on_pre_enter(self, *args):
        # Reset button background color when screen is entered
        buttons = self.ids.tf_buttons.children
        for button in buttons:
            button.md_bg_color = [1, 1, 1, 1]  # Set all buttons to white initially

    def on_leave(self, *args):
        # Reset button background color when leaving the screen
        self.on_pre_enter()

    def show_text_input_dialog(self):
        content = MDTextField()
        
        # Customize title label
        title_text = "[size=16][b]Change point value for all questions[/b][/size]"
        
        dialog = MDDialog(
            title=title_text,
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(
                    text="CANCEL", 
                    on_release=lambda *args: dialog.dismiss()
                ),
                MDFlatButton(
                    text="OK",
                    on_release=lambda *args: self.process_text_input(content.text, dialog),
                ),
            ],
        )
        dialog.open()

    def process_text_input(self, text, dialog):
        print("Entered text:", text)
        # Here you can do something with the entered text, like updating the UI, etc.
        dialog.dismiss()



class IDScreen(Screen):
    pass

        
class App(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Indigo"
        screen = Builder.load_string(KV)
        return screen
    
    #dialog box and text field
    def show_text_input_dialog(self):
        content = MDTextField()
    
        # Customize title label
        title_text = "[size=16][b]Change point value for all questions[/b][/size]"
    
        dialog = MDDialog(
            title=title_text,
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(
                    text="CANCEL", 
                    on_release=lambda *args: dialog.dismiss()
                ),
                MDFlatButton(
                    text="OK",
                    on_release=lambda *args: self.process_text_input(content.text, dialog),
                ),
        ]   ,
        )
        dialog.open()


    def process_text_input(self, text, dialog):
        print("Entered text:", text)
        # Here you can do something with the entered text, like updating the UI, etc.
        dialog.dismiss()
    
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


App().run()