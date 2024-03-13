from kivy.lang.builder import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from datetime import datetime
from kivymd.uix.button import MDFlatButton,MDRaisedButton, MDRectangleFlatButton
from kivymd.uix.card import MDSeparator
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.floatlayout import MDFloatLayout
#from utilities.sheet.sheet import BubbleSheet

KV = '''
CustomScreenManager:
    AnswerSheetScreen:

<AnswerSheetScreen>:
    name: 'answer_sheet'
    orientation: 'vertical'

    MDTopAppBar:
        title: "QuickMark"
        elevation: 0
        pos_hint: {"top": 1}

    ScrollView:
        do_scroll_y: False 
        pos_hint: {"top":.9, "center_x": .5}

        BoxLayout:
            orientation: 'vertical'
            padding: dp(16)
            spacing: dp(10)
            size_hint_y: None
            height: self.minimum_height

            MDGridLayout:
                cols: 2
                spacing: dp(10)
                size_hint: None, None
                pos_hint: {'center_x':0.15}

                MDGridLayout:
                    cols: 2
                    size_hint: None, None
                    width: dp(200) 
                    height: dp(50)
                    
                    MDCheckbox:
                        id: mcq_checkbox
                        size_hint: None, None
                        size: dp(48), dp(48)
                        on_active: app.show_text_field(self.active, 'mcq')

                    MDLabel:
                        text: "Multiple Choice"
                        size_hint: None, None
                        halign: 'left'
                        size: dp(200), dp(48)


                MDTextField:
                    id: mcq_textfield
                    hint_text: "Number of questions"
                    input_filter: 'int'
                    mode: "rectangle"
                    size_hint: None, None
                    width: dp(400) 
                    height: dp(48)
                    multiline: False
                    disabled: not mcq_checkbox.active

                MDGridLayout:
                    cols: 2
                    spacing: dp(10)

                    MDGridLayout:
                        cols: 2
                        size_hint: None, None
                        width: dp(200) 
                        height: dp(50)
                        
                        MDCheckbox:
                            id: tf_checkbox
                            size_hint: None, None
                            size: dp(48), dp(48)
                            on_active: app.show_text_field(self.active, 'tf')

                        MDLabel:
                            text: "True or False"
                            size_hint: None, None
                            halign: 'left'
                            size: dp(200), dp(48)


                    MDTextField:
                        id: tf_textfield
                        hint_text: "Number of questions"
                        input_filter: 'int'
                        mode: "rectangle"
                        size_hint: None, None
                        width: dp(400) 
                        height: dp(48)
                        multiline: False
                        disabled: not tf_checkbox.active

                    MDGridLayout:
                        cols: 2
                        size_hint: None, None
                        width: dp(200) 
                        height: dp(50)
                        
                        MDCheckbox:
                            id: ident_checkbox
                            size_hint: None, None
                            size: dp(48), dp(48)
                            on_active: app.show_text_field(self.active, 'ident')

                        MDLabel:
                            text: "Identification"
                            size_hint: None, None
                            halign: 'left'
                            size: dp(200), dp(48)


                    MDTextField:
                        id: ident_textfield
                        hint_text: "Number of questions"
                        input_filter: 'int'
                        mode: "rectangle"
                        size_hint: None, None
                        width: dp(400) 
                        height: dp(48)
                        multiline: False
                        disabled: not ident_checkbox.active

    Widget:
        size_hint_y: None
        height: dp(48)

    MDRectangleFlatButton:
        text: "GENERATE"
        size_hint: None, None
        size: dp(200), dp(48)
        pos_hint: {'top':0.52,'center_x': 0.5}
        #on_press: app.generate_answer_sheet()

    Image:
        id: generated_image
        size_hint: 1, None
        height: dp(210)  # Set the height of the image as needed
        pos_hint: {'top':0.45,'center_x': 0.5}

    MDRectangleFlatButton:
        id: download
        text: "Download HTML"
        size_hint: None, None
        size: dp(200), dp(36)
        pos_hint: {'top':0.08,'center_x': 0.5}
        on_press: app.download_html()
        disabled: True

'''

class AnswerSheetScreen(Screen):
    pass


class CustomScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.transition = NoTransition()


class App(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Purple"
        screen = Builder.load_string(KV)
        return screen

    def show_text_field(self, active, checkbox_type):
    # Enable/disable text fields based on checkbox state
        if checkbox_type == 'mcq':
            self.root.get_screen('answer_sheet').ids.mcq_textfield.disabled = not active
        elif checkbox_type == 'tf_textfield':
            self.root.get_screen('answer_sheet').ids.tf_textfield.disabled = not active
        elif checkbox_type == 'ident':
            self.root.get_screen('answer_sheet').ids.ident_textfield.disabled = not active

    def generate_answer_sheet(self):
        mcq_questions = int(self.root.get_screen('answer_sheet').ids.mcq_textfield.text) if self.root.get_screen('answer_sheet').ids.mcq_checkbox.active else 0
        tf_questions = int(self.root.get_screen('answer_sheet').ids.tf_textfield.text) if self.root.get_screen('answer_sheet').ids.tf_checkbox.active else 0
        ident_questions = int(self.root.get_screen('answer_sheet').ids.ident_textfield.text) if self.root.get_screen('answer_sheet').ids.ident_checkbox.active else 0
        sheet = BubbleSheet(mc_num = mcq_questions,tf_num = tf_questions, idtf_num = ident_questions,header_name = "test")

        #sheet.save_template_as_img(r"template.png")
        self.root.get_screen('answer_sheet').ids.generated_image.source = r"assets\template.png"
        self.root.get_screen('answer_sheet').ids.download.disabled = False

    def download_html(self):
        # Add your download logic here
        pass

App().run()