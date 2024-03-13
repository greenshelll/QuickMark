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
from kivymd.uix.label import MDLabel
import pickle
from kivymd.uix.dialog import MDDialog
from utilities.misc.filesystem import *
from utilities.misc.search import rate_similarity
from kivy.core.window import Window
from kivymd.uix.list import MDList, TwoLineListItem
from kivy.clock import Clock
from kivymd.toast import toast
from kivy.metrics import dp
from kivymd.uix.toolbar import MDTopAppBar

KV = '''
CustomScreenManager:
    HomeScreen:
    NameScreen:
    CheckScreen:
    MCScreen:
    IDScreen:
    TFScreen:
    AnalysisScreen:
    AnswerSheetScreen:

<HomeScreen>:
    name: 'home'

    canvas.before:
        Color:
            rgba: 1, 1, 1, 1  # White color
        Rectangle:
            size: self.size
            pos: self.pos
    
    MDTopAppBar:
        title: "QuickMark"
        pos_hint: {"top": 1,}
        right_action_items: [["plus-circle", lambda x: print(setattr(root.manager, 'current', 'name'),root.add_new_sheet(),'hello world')]]
        elevation: 0


    MDStackLayout:
        height: self.minimum_height
        pos_hint: {'center_x': 0.5}
        MDTopAppBar:
            title: "QuickMark"
            right_action_items: [["plus-circle", lambda x: print(setattr(root.manager, 'current', 'name'),root.add_new_sheet(),'hello world')]]
            elevation: 0
        BoxLayout:
            size_hint: (None,None)
            orientation: 'horizontal'
            size_y: 20
            padding: (40,0)
            size_hint: (0.95,None)
            MDTextField:
                hint_text: "Search..."
                height: dp(20)
                padding: (40, 40)
                size_hint: (1,None)
                #on_text: root.word_search(*args)
        ScrollView:
            id: scroll_view
            size_hint: (1, None)
            MDList:
                id: saved_list
                size_hint_y: None
                height: self.minimum_height

                 
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
        on_text_validate: root.rename()
        on_text: root.capitalize(*args)
    
    MDFloatLayout:
        MDRaisedButton:
            id: save_button
            text: "SAVE"
            pos_hint:{"top":.85, "center_x": .7}
            on_release: root.rename()
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
        on_release: root.manager.current = 'check'
          

    MDRectangleFlatButton:
        text: "ANALYSIS"
        pos_hint: {"top":.61, "center_x": .5}
        on_release: root.manager.current = 'analysis'
              

    MDSeparator:
        pos_hint: {"top":.5, "center_x": .5}
        size_hint_y: None
        height: dp(1)  

    MDLabel:
        text:"Answer Sheet"
        halign: "center"
        pos_hint: {"center_y":.48}

    MDRectangleFlatButton:
        text: "EDIT ANSWER SHEET"
        pos_hint: {"top":.43, "center_x": .5}
        on_release:  root.prepare_answer_sheet(); root.manager.current = 'answer_sheet'

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
        on_release: root.prepare_mc_keys() ; root.manager.current = 'MC'

    MDRectangleFlatButton:
        text: "TRUE OR FALSE"
        pos_hint: {"top":.17, "center_x": .5}
        on_release: root.prepare_tf_keys() ;root.manager.current = 'TF'

    MDRectangleFlatButton:
        text: "IDENTIFICATION"
        pos_hint: {"top":.1, "center_x": .5}
        on_release: root.manager.current = 'ID'

        CustomScreenManager:
    
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
                        on_active: root.show_text_field(self.active, 'mcq')

                    MDLabel:
                        text: "Multiple Choice"
                        size_hint: None, None
                        halign: 'left'
                        size: dp(200), dp(48)


                MDTextField:
                    id: mcq_textfield
                    hint_text: "count"
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
                            on_active: root.show_text_field(self.active, 'tf')

                        MDLabel:
                            text: "True or False"
                            size_hint: None, None
                            halign: 'left'
                            size: dp(200), dp(48)


                    MDTextField:
                        id: tf_textfield
                        hint_text: "count"
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
                            on_active: root.show_text_field(self.active, 'ident')

                        MDLabel:
                            text: "Identification"
                            size_hint: None, None
                            halign: 'left'
                            size: dp(200), dp(48)


                    MDTextField:
                        id: ident_textfield
                        hint_text: "count"
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
        text: "APPLY"
        size_hint: None, None
        size: dp(200), dp(48)
        pos_hint: {'top':0.52,'center_x': 0.5}
        on_release: root.apply_count()

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


<MCScreen>:
    name: 'MC'
    
    
    MDBoxLayout:
        id: mc_box_all
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
        id: tf_box_all
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
def scan_object(obj, visited=None):
    if visited is None:
        visited = set()

    if id(obj) in visited:
        return
    visited.add(id(obj))

    if isinstance(obj, dict):
        for key, value in obj.items():
            print(f"Dictionary key: {key}, value: {value}")
            if isinstance(value, (list, tuple, dict, set)):
                scan_object(value, visited)
            elif hasattr(value, "__dict__"):
                scan_object(vars(value), visited)
    elif isinstance(obj, (list, tuple, set)):
        for item in obj:
            scan_object(item, visited)
    elif hasattr(obj, "__dict__"):
        for key, value in vars(obj).items():
            print(f"Attribute: {key}, value: {value}")
            if hasattr(value, "__dict__"):
                scan_object(vars(value), visited)

fs = FileSystem()

class Instance(TwoLineListItem):
    def __init__(self, **kwargs):
        super(Instance, self).__init__(**kwargs)
        self.select_id = None
        self.manager = None
    
    def on_release(self, *args, **kwargs):
        #fs.get_sheet(self.select_id).name = str(fs.get_sheet(self.select_id).name)
        name_screen = self.manager.get_screen('name')
        name_screen.ids.text_field.text = fs.get_sheet(self.select_id).name
        fs.open_index = self.select_id
        self.manager.current = 'name'
        
class CustomScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.transition = NoTransition()

import numpy as np
import threading
"""MDBoxLayout:
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


        Returns:
            _type_: _description_
"""


class MCInstanceBox(BoxLayout):
    def __init__(self, number, **kwargs):
        super(MCInstanceBox, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        self.spacing = dp(2)
        self.size_hint_x = None
        self.size_hint_y = None
        self.buttons = []
        self.number = number
        self.true_answer = fs.sheets[fs.open_index].answer_key.mc.items[self.number].answer_key
        print(self.true_answer)
        # Add label
        label = MDLabel(text=f'  {number+1}.', adaptive_width=True)
        self.add_widget(label)

        # Add buttons
        for letter in ['A','B','C','D']:
            button = MDRoundFlatButton(text=letter, id=letter)
            button.size_hint = (None, None)  # Ensure size_hint is set before width and height
            button.width = self.width * 0.05  # Set button width to 10% of MCInstanceBox width
            button.height = self.height * 0.04  # Set button height to 4% of MCInstanceBox height
            #button.bind(size=self.update_button_size)  # Bind size changes to update_button_size method
            self.add_widget(button)
            
            
            self.buttons.append(button)
            self.toggle_button_state(button,self.true_answer)
            button.bind(on_release=lambda btn=button: self.toggle_button_state(btn))
    def toggle_button_state(self,button, initialize=None):
        # Deselect all buttons
        buttons = self.buttons
        #print(button.text)
        for btn in buttons:
            if btn.text != button.text if initialize is None else btn.text != initialize:
                btn.md_bg_color = [1, 1, 1, 1]  # Revert background color to white
            else:
                btn.md_bg_color = [0.5,0.5,0.5,1]
                fs.sheets[fs.open_index].answer_key.mc.items[self.number].answer_key = btn.text
        
        
        # Highlight the pressed button
            
                
class TFInstanceBox(BoxLayout):
    def __init__(self, number, **kwargs):
        super(TFInstanceBox, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        self.spacing = dp(2)
        self.size_hint_x = None
        self.size_hint_y = None
        self.buttons = []
        self.number = number
        self.true_answer = fs.sheets[fs.open_index].answer_key.tf.items[self.number].answer_key
        print(self.true_answer)
        # Add label
        label = MDLabel(text=f'  {number+1}.', adaptive_width=True)
        self.add_widget(label)

        # Add buttons
        for letter in ['T','F']:
            button = MDRoundFlatButton(text=letter, id=letter)
            button.size_hint = (None, None)  # Ensure size_hint is set before width and height
            button.width = self.width * 0.05  # Set button width to 10% of MCInstanceBox width
            button.height = self.height * 0.04  # Set button height to 4% of MCInstanceBox height
            #button.bind(size=self.update_button_size)  # Bind size changes to update_button_size method
            self.add_widget(button)
            
            
            self.buttons.append(button)
            self.toggle_button_state(button,self.true_answer)
            button.bind(on_release=lambda btn=button: self.toggle_button_state(btn))
            



    def toggle_button_state(self,button, initialize=None):
        # Deselect all buttons
        buttons = self.buttons
        #print(button.text)
        for btn in buttons:
            if btn.text != button.text if initialize is None else btn.text != initialize:
                btn.md_bg_color = [1, 1, 1, 1]  # Revert background color to white
            else:
                btn.md_bg_color = [0.5,0.5,0.5,1]
                fs.sheets[fs.open_index].answer_key.tf.items[self.number].answer_key = btn.text
        
        
        # Highlight the pressed button

  
class HomeScreen(Screen):
    def add_new_sheet(self):
        print("ADDING NEW SHEET")
        fs.add_sheet()
        fs.get_sheet(-1).name = str(len(fs.sheets)) # gets last added sheet (index "-1")
        name_screen = self.manager.get_screen('name')
        fs.get_sheet(-1).name = str('unnamed')
        name_screen.ids.text_field.text = fs.get_sheet(-1).name 
        #fs.save()
        self.add_item_to_list()
        toast("New Sheet Added.", (1,0,1,0.2), 1)

    def word_search(self, instance, text):
        self.defined_sheets = []
        def thread_search(self, instance,text):
            words = np.unique([x.name for x in fs.sheets])

            # Rate similarity for each word and sort them
            rated_words = rate_similarity(words, text)
            sorted_words = sorted(rated_words, key=rated_words.get)

            # Populate defined_sheets list based on the sorted words
            self.defined_sheets = []
            for word in sorted_words:
                for sheet in fs.sheets:
                    if sheet.name == word:
                        self.defined_sheets.append(sheet)

            # Print the sorted sheets
            for sheet in self.defined_sheets:
                print(sheet.name)
        if not self.thread_lock.acquire(blocking=False):
            # Lock is already acquired, meaning a thread is running
            print("Thread is already running")
            return
        try:
            # Start the thread
            self.thread = threading.Thread(target=lambda: thread_search(self, instance,text))
            self.thread.start()
        except Exception:
            # Release the lock if an exception occurs
            pass
        self.thread_lock.release()
        self.add_item_to_list(self.defined_sheets)


        
    def add_item_to_list(self, defined_sheets=[]):
        print("ADDING TO LIST")
        saved_list = self.ids.saved_list
        saved_list.clear_widgets()
        for sheet_i in range(len(fs.sheets)):
            if len(defined_sheets) == 0:
                sheet = fs.sheets[sheet_i]
            else:
                sheet = defined_sheets[sheet_i]
            sheet_name = sheet.name
            instance = Instance(text=sheet_name)
            instance.select_id = sheet_i
            instance.manager = self.manager
            instance.secondary_text = 'Date Created: '+ str(sheet.date_created).split(' ')[0]
            saved_list.add_widget(instance)

        layout = BoxLayout(orientation='vertical', padding=20) # Add padding around the layout

        # Create an MDLabel
        label = MDLabel(
            text="\n--end--\n",
            halign="center",  # Center the text horizontally
            theme_text_color="Secondary",  # Set the color to gray
            size_hint_y=None,
            height=20,  # Adjust the height of the label
            padding=(20, 10) , # Add padding around the label
            pos_hint={"center_y": 0.5} 
        )
        saved_list.add_widget(MDLabel(
                    text="\n\n",
                    halign="center",  # Center the text horizontally
                    theme_text_color="Secondary",  # Set the color to gray
                    size_hint_y=None,
                    height=20,  # Adjust the height of the label
                    padding=(20, 10) , # Add padding around the label
                    pos_hint={"center_y": 0.5} 
                ))
        saved_list.add_widget(label)
        
        self.ids.scroll_view.height = Window.height-(130)
        


    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        self.thread = None
        self.thread_lock = threading.Lock()

class AnalysisScreen(Screen):
    percentage = 0.5  # Example percentage value

    def update_percentage(self, value):
        try:

            percentage = float(value) / 100
            if 0 <= percentage <= 1:
                self.percentage = percentage
            else:
                print("Percentage must be between 0 and 100.")
        except ValueError:
            print("Invalid input. Please enter a valid percentage.")

class NameScreen(Screen):
    def __init__(self, **kwargs):
        super(NameScreen, self).__init__(**kwargs)

    def prepare_mc_keys(self):
        mc_screen = self.manager.get_screen('MC')
        answer_key = fs.sheets[fs.open_index].answer_key.mc
        mc_screen.instances = []
        #mc_screen.ids.mc_box_all.clear_widgets()
        widgets_to_remove = []
    
        # Iterate through the children of tf_box_all
        for child in mc_screen.ids.mc_box_all.children:
            # Check if the child is an instance of TopAppBar
            if not isinstance(child, MDTopAppBar):
                # If it's not a TopAppBar, add it to the list of widgets to be removed
                widgets_to_remove.append(child)
        
        # Remove the widgets from tf_box_all
        for widget in widgets_to_remove:
            mc_screen.ids.mc_box_all.remove_widget(widget)
        increment = 0
        for answer_item in answer_key.get_items():
            
            instance = MCInstanceBox(increment)
            mc_screen.ids.mc_box_all.add_widget(instance)
            mc_screen.instances.append(instance)
            increment += 1
        print(mc_screen.instances)

    def prepare_tf_keys(self):
        tf_screen = self.manager.get_screen('TF')
        answer_key = fs.sheets[fs.open_index].answer_key.tf
        tf_screen.instances = []
        #tf_screen.ids.tf_box_all.clear_widgets()
        widgets_to_remove = []
    
        # Iterate through the children of tf_box_all
        for child in tf_screen.ids.tf_box_all.children:
            # Check if the child is an instance of TopAppBar
            if not isinstance(child, MDTopAppBar):
                # If it's not a TopAppBar, add it to the list of widgets to be removed
                widgets_to_remove.append(child)
        
        # Remove the widgets from tf_box_all
        for widget in widgets_to_remove:
            tf_screen.ids.tf_box_all.remove_widget(widget)
        increment = 0
        for answer_item in answer_key.get_items():
            
            instance = TFInstanceBox(increment)
            tf_screen.ids.tf_box_all.add_widget(instance)
            tf_screen.instances.append(instance)
            increment += 1
        print(tf_screen.instances)
    
    def prepare_answer_sheet(self):
        sheet_screen = self.manager.get_screen('answer_sheet')
        answer_key = fs.sheets[fs.open_index].answer_key
        sheet_screen.ids.mcq_textfield.text = str(len(answer_key.mc.get_items()))
        sheet_screen.ids.tf_textfield.text = str(len(answer_key.tf.get_items()))
        sheet_screen.ids.ident_textfield.text = str(len(answer_key.idtf.get_items()))
        sheet_screen.ids.mcq_checkbox.active = True if len(answer_key.mc.get_items()) > 0 else False
        sheet_screen.ids.tf_checkbox.active = True if len(answer_key.tf.get_items()) > 0 else False
        sheet_screen.ids.ident_checkbox.active = True if len(answer_key.idtf.get_items()) > 0 else False
    
    def rename(self):
        print("RENAMING")
        index = fs.open_index
        current_name = self.ids.text_field.text
        fs.sheets[index].name = current_name
        #fs.save()
        home_screen = self.manager.get_screen('home')
        home_screen.add_item_to_list()
        toast("Renamed successfully.", (1,0,1,0.2), 1)


    def capitalize(self, instance, text):
        text = text.upper()
        self.ids.text_field.text = text

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
        #buttons = self.ids.mc_buttons.children
        #for button in buttons:
        #   button.md_bg_color = [1, 1, 1, 1]  # Set all buttons to white initially
        pass

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

class CheckScreen(Screen):
    def cam_off(self):
        self.remove_widget(self.camera_widget)
        self.camera_widget.remove_camera = True
        self.camera_widget.camera.remove_from_cache()
        self.camera_widget.camera.play = False
        del self.camera_widget.camera._camera
        self.cam_is_on = False


    def cam_on(self):
        mc = fs.sheets[fs.open_index].answer_key.mc
        tf = fs.sheets[fs.open_index].answer_key.tf
        idtf = fs.sheets[fs.open_index].answer_key.idtf
        mc_answers = [x.answer_key for x in mc.get_items()]
        tf_answers = [x.answer_key for x in tf.get_items()]
        idtf_answers = [x.answer_key for x in idtf.get_items()]
        print(mc,tf,idtf)
        self.camera_widget = CameraWidget()
        """self.camera_widget = CameraWidget(mcq_correct=mc_answers, 
                                          tf_correct=tf_answers,
                                          idtf_correct=idtf_answers)"""
        self.add_widget(self.camera_widget)
    
        self.cam_is_on = True


    def switch_cam(self,*args,**kwargs):
        if self.cam_is_on == False:
            self.cam_on()
        else:
            self.cam_off()
            
            

    def __init__(self,**kwargs):
        super(CheckScreen, self).__init__(**kwargs)
        self.cam_is_on = False


class AnswerSheetScreen(Screen):
    def apply_count_for_type(self, key_type):
        answer_key = fs.sheets[fs.open_index].answer_key
        textfield = None
        count = 0
        if key_type=='mc':
            answer_key = answer_key.mc
            textfield = self.ids.mcq_textfield
        elif key_type =='tf':
            answer_key = answer_key.tf
            textfield = self.ids.tf_textfield
        elif key_type=='idtf':
            answer_key = answer_key.idtf
            textfield = self.ids.ident_textfield

        if textfield.disabled == True or textfield.text == '':
            count = 0
        else:
            count = int(textfield.text)
        print(textfield.disabled)
        print(f'{key_type} item count: {count}')
        print('showing',answer_key.show_items)
        answer_key.set_items(count)
        toast("Sheet Updated.")
    
    def apply_count(self):
        self.apply_count_for_type('mc')
        self.apply_count_for_type('tf')
        self.apply_count_for_type('idtf')
    
    def show_text_field(self, active, checkbox_type):
    # Enable/disable text fields based on checkbox state
        if checkbox_type == 'mcq':
            self.manager.get_screen('answer_sheet').ids.mcq_textfield.disabled = not active
        elif checkbox_type == 'tf_textfield':
            self.manager.get_screen('answer_sheet').ids.tf_textfield.disabled = not active
        elif checkbox_type == 'ident':
            self.manager.get_screen('answer_sheet').ids.ident_textfield.disabled = not active


class MCScreen(Screen):
    pass

def autosave():
    fs.save()
    autosave_sched()

def autosave_sched():
    Clock.schedule_once(lambda x:threading.Thread(target=lambda: autosave()).start(),0.01) 

class App(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Purple"
        self.screen = Builder.load_string(KV)
        return self.screen
    
    def on_start(self):
        # Run a function after the screen has been loaded
        home_screen = self.root.get_screen('home')
        home_screen.add_item_to_list()
        autosave_sched()
        from kivy.base import EventLoop
        EventLoop.window.bind(on_keyboard=self.hook_keyboard)
    
    def screen_manager_func(self):
        dummy = self.root.get_screen('home')
        if dummy.manager.current == 'home':
            self.stop()
        elif dummy.manager.current == 'name':
            dummy.manager.current = 'home'
        elif dummy.manager.current =='check':
            try:
                if self.root.get_screen('check').cam_is_on == True:
                    self.root.get_screen('check').cam_off()
                else:
                    dummy.manager.current = 'name'
            except Exception as e:
                print(e)
                pass
            
        else:
            dummy.manager.current = 'name'
            

    def hook_keyboard(self, window, key, *largs):
        if key == 27:
            # do what you want, return True for stopping the propagation
            self.screen_manager_func()
            return True 

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