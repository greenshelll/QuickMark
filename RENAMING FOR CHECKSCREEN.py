# LIBRARIES
import numpy as np
import threading
from datetime import datetime
import shutil
import os
import time
try:
    from android.storage import primary_external_storage_path
    android_storage = primary_external_storage_path()
    from jnius import autoclass
    from jnius import cast
    
    on_android = True
except Exception as e:
    on_android = False

# LOCAL FILES/MODULES
from utilities.misc.util4image import fit_score,stich_all_image as stitch_sheet
from utilities.misc.filesystem import *
from utilities.misc.searchsystem import *
from screens.camera import CameraWidget

# KIVY/KIVYMD IMPORTS
#kivymd misc
from kivy.lang.builder import Builder
from kivymd.app import MDApp
from kivy.clock import Clock
from kivymd.toast import toast
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.core.image import Image as CoreImage
from kivy.properties import DictProperty

#kivymd.uix
from kivymd.uix.list import IconLeftWidget, IconLeftWidgetWithoutTouch, IconRightWidgetWithoutTouch

from kivymd.uix.dialog import MDDialog
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFlatButton,MDRaisedButton, MDRectangleFlatButton, MDRoundFlatButton, MDFillRoundFlatButton, MDFloatingActionButtonSpeedDial
from kivymd.uix.card import MDSeparator
from kivymd.uix.stacklayout import MDStackLayout
from kivymd.uix.card import MDCard
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.list import MDList, TwoLineListItem, TwoLineIconListItem, TwoLineAvatarIconListItem
from kivy.uix.image import Image
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
#kivy.uix
from kivy.uix.boxlayout import BoxLayout

Window.size= (288,640)

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
    OneCheckScreen:

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
        left_action_items: [['menu', lambda x: app.screen_manager_func()]]
        right_action_items: [["plus-circle", lambda x: print(setattr(root.manager, 'current', 'name'),root.add_new_sheet(),'hello world')]]
        elevation: 0


    MDStackLayout:
        md_bg_color: (0.95,0.95,0.95,1)
        height: self.minimum_height
        pos_hint: {'center_x': 0.5}
        MDTopAppBar:
            title: "QuickMark"
            left_action_items: [['close-box', lambda x: app.screen_manager_func()]]
            right_action_items: [["plus-circle", lambda x: print(setattr(root.manager, 'current', 'name'),root.add_new_sheet(),'hello world')]]
            elevation: 0
        BoxLayout:
            canvas.before:
                Color:
                    rgba: 0.95,0.95,0.95,1 # Set the background color here
                Rectangle:
                    pos: self.pos
                    size: root.size[0], self.size[1]
            size_hint: (None,None)
            orientation: 'horizontal'
            height: dp(25)
            padding: (20,10)
            size_hint: (0.95,None)

            MDLabel:
                text: "Home > "
                font_size: dp(10)
                pos_hint: {'center_x':0}
                

        BoxLayout:
            canvas.before:
                Color:
                    rgba: 1, 1, 1, 1  # Set the background color here
                Rectangle:
                    pos: self.pos
                    size: root.size[0], self.size[1]
            size_hint: (None,None)
            orientation: 'horizontal'
            height: dp(80)
            padding: (20,10)
            size_hint: (0.95,None)
            
            MDTextField:
                md_bg_color: (1,1,1,1)
                icon_left: 'magnify'
                hint_text: "Search..."
                height: dp(20)
                padding: (40, 40)
                size_hint: (0.9,None)
                on_text: root.word_search(*args)

                
        BoxLayout:
            id: box_label
            canvas.before:
                Color:
                    rgba: 0.95,0.95,0.95,1 # Set the background color here
                Rectangle:
                    pos: self.pos
                    size: root.size[0], dp(10)
            size_hint: (None,None)
            orientation: 'horizontal'
            size_hint: (1,None)
            height: 100
            MDLabel:
                id: empty_label
                text: ""
                halign:"center"  # Center the text horizontally
                theme_text_color:"Secondary" # Set the color to gray
                size_hint_y: None
                height:20
                padding:(20, 10)  # Add padding around the label
                pos_hint:{"center_y": 0.5} 
        ScrollView:
            id: scroll_view
            size_hint: (1, None)
            
            MDList:
                id: saved_list
                size_hint_y: None
                height: self.minimum_height
                md_bg_color: (1,1,1,1)
                padding: 0  # Set padding to 0
                spacing: 0 

        


                                 
<NameScreen>:
    name: 'name'

    MDLabel:
        id: display_label
        text: ""
        halign: "center"
        pos_hint: {"top": 1.33}
    
    MDStackLayout:
        md_bg_color: (0.95,0.95,0.95,1)
        height: self.minimum_height
        pos_hint: {'center_x': 0.5}
        MDTopAppBar:
            title: "QuickMark"
            left_action_items: [['chevron-left', lambda x: app.screen_manager_func()]]
            right_action_items: [["plus-circle", lambda x: print(setattr(root.manager, 'current', 'name'),root.add_new_sheet(),'hello world')]]
            elevation: 0
        BoxLayout:
            canvas.before:
                Color:
                    rgba: 0.95,0.95,0.95,1 # Set the background color here
                Rectangle:
                    pos: self.pos
                    size: root.size[0], self.size[1]
            size_hint: (None,None)
            orientation: 'horizontal'
            height: dp(25)
            padding: (20,10)
            size_hint: (0.95,None)

            MDLabel:
                text: "Home > Sheet > "
                font_size: dp(10)
                pos_hint: {'center_x':0}
        
        BoxLayout:
            canvas.before:
                Color:
                    rgba: 1, 1, 1, 1  # Set the background color here
                Rectangle:
                    pos: self.pos
                    size: root.size[0], self.size[1]
            size_hint: (None,None)
            orientation: 'vertical'
            height: dp(100)
            padding: (20,20)
            size_hint: (0.95,None)
                
    
            BoxLayout:
                size_hint: 1,None
                padding: (25,25)
                spacing: dp(10)
                orientation: 'horizontal'
                MDTextField:
                    id: text_field
                    mode: "fill"
                    multiline: False
                    size_hint_y: None
                    size_hint_x: None
                    height: dp(20)
                    width: "250dp"
                    pos_hint: {"center_y":0.5, "center_x": .5}
                    hint_text: "Sheet Name"
                    on_text_validate: root.rename()
                    on_text: root.capitalize(*args)
            
                MDIconButton:
                    id: save_button
                    icon: 'square-edit-outline'
                    pos_hint:{"center_y":.5}
                    on_release: root.rename()
                    elevation: 0

            MDLabel:
                text: 'Date Created: YYYY-MM-DD'
                color: (0.5,0.5,0.5,1)
                pos_hint: {'center_x':0.5}
                font_size: dp(10)
        BoxLayout:
            id: box_label
            canvas.before:
                Color:
                    rgba: 0.95,0.95,0.95,1 # Set the background color here
                Rectangle:
                    pos: self.pos
                    size: root.size[0], dp(10)
            size_hint: (None,None)
            orientation: 'horizontal'
            
            size_hint: (1,None)
            height: dp(10)

        ScrollView:
            id: scroll_view
            size_hint: (1, 1)

            MDList:
                id: saved_list
                size_hint_y: None
                height: self.minimum_height
                md_bg_color: (1,1,1,1)
                padding: 0  # Set padding to 0
                spacing: 0 
                
                TwoLineAvatarIconListItem:
                    text: 'Check Papers'
                    secondary_text: 'Review and record student marks.'
                    secondary_font_style: 'Caption'
                    on_release: root.manager.current = 'onecheck'
                    IconLeftWidgetWithoutTouch:
                        icon: "paperclip-check"
                    IconRightWidgetWithoutTouch:
                        icon: "chevron-right"

                TwoLineAvatarIconListItem:
                    text: 'Analysis'
                    secondary_text: 'Conduct item analysis.'
                    secondary_font_style: 'Caption'
                    on_release: root.manager.current = 'analysis'
                    IconLeftWidgetWithoutTouch:
                        icon: "google-analytics"
                    IconRightWidgetWithoutTouch:
                        icon: "chevron-right"

                TwoLineAvatarIconListItem:
                    text: 'Answer Sheet'
                   
                    secondary_text: 'View and edit answer sheet.'
                    secondary_font_style: 'Caption'
                    on_release: root.manager.current = root.prepare_answer_sheet(); root.manager.current = 'answer_sheet'
                    IconLeftWidgetWithoutTouch:
                        icon: "view-dashboard-edit-outline"
                TwoLineAvatarIconListItem:
                    text: 'Answer Key'
                    secondary_text: 'View or change answer keys.'
                    bg_color: 0.95,0.95,0.95,0.95
                    secondary_font_style: 'Caption'
                    IconLeftWidgetWithoutTouch:
                        icon: "key-outline"
                    IconRightWidgetWithoutTouch:
                        icon: "chevron-right"
                OneLineAvatarIconListItem:
                    text: 'Multiple Choice'
                    IconRightWidgetWithoutTouch:
                        icon: "chevron-right"
                OneLineAvatarIconListItem:
                    text: 'True or False'
                    IconRightWidgetWithoutTouch:
                        icon: "chevron-right"
                OneLineAvatarIconListItem:
                    id: idtf_key
                    text: 'Identification'
                
                    on_release: lambda x: print("HELLO")
                    IconRightWidgetWithoutTouch:
                        id: idtf_icon
                        icon: "chevron-right"
                    
                
                
                    
                    


        MDLabel:
            text:"Appraisal"
            halign: "center"
            pos_hint: {"center_y":.73}
        
        MDRectangleFlatButton:
            text: "CHECK PAPERS" 
            on_release: root.manager.current = 'onecheck'
            _min_width: 200
            

        MDRectangleFlatButton:
            text: "ANALYSIS"
            pos_hint: {"top":.61, "center_x": .5}
            on_release: root.manager.current = 'analysis'
            _min_width: 200
                

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
            on_release: root.prepare_mc_keys() ; root.manager.current = 'MC'
            _min_width: 200

        MDRectangleFlatButton:
            text: "TRUE OR FALSE"
            pos_hint: {"top":.17, "center_x": .5}
            on_release: root.prepare_tf_keys() ;root.manager.current = 'TF'
            _min_width: 200

        MDRectangleFlatButton:
            text: "IDENTIFICATION"
            pos_hint: {"top":.1, "center_x": .5}
            on_release: root.manager.current = 'ID'
            _min_width: 200

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
        id: apply_btn
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
    
    MDBoxLayout:
        orientation: 'horizontal'
        size_hint: None, 1
        pos_hint: {'center_x': 0.4}
        padding: dp(20)
        spacing: dp(10)

        MDRectangleFlatButton:
            id: download
            text: "Export"
            size_hint: 1, None
            size: dp(200), dp(36)
            pos_hint: {'center_x': 0.5}
            on_release: root.open_file_manager()

        MDRectangleFlatButton:
            id: download
            text: "Share"
            size_hint: 1, None
            size: dp(200), dp(36)
            pos_hint: {'center_x': 0.5}
            on_release: root.share()
    


<CheckScreen>:
    name: 'check'

    MDTopAppBar:
        title: "QuickMark"
        right_action_items: [['file-export']]
        left_action_items: [['chevron-left', lambda x: app.screen_manager_func()]]
        elevation: 0
        pos_hint: {"top": 1}

    MDBoxLayout:
        orientation: 'vertical'
        spacing: dp(5)
        pos_hint: {'top':0.5, 'center_x': 0.5}
        size_hint: 1,0.5
        padding: 20

        MDTextField:
            id: check_text_field
            mode: "fill"
            multiline: False
            size_hint_y: None
            size_hint_x: None
            height: dp(20)
            width: "250dp"
            pos_hint: {"center_y":0.5, "center_x": .5}
            hint_text: "Sheet Name"
            

        MDLabel:
            text: 'Scores'
            theme_text_color: 'Primary'
            font_size: dp(20)
            size_hint_y: None
            size_hint_x: None
            height: dp(40)

        MDLabel:
            id: mc_indicator
            text: 'Multiple Choice: '
            theme_text_color: 'Secondary'
            font_size: dp(15)
            size_hint_y: None
            height: dp(40)

        MDLabel:
            id: tf_indicator
            text: 'True or False: '
            theme_text_color: 'Secondary'
            font_size: dp(15)
            size_hint_y: None
            height: dp(40)

        MDLabel:
            id: idtf_indicator
            text: 'Identification: '
            theme_text_color: 'Secondary'
            font_size: dp(15)
            size_hint_y: None
            height: dp(40)
    
    MDFloatingActionButton:
        id: plus_button
        icon: 'plus'
        on_release: app.root.get_screen('check').add_new_sheet()  # Call add_new_sheet method from CheckScreen        
        pos_hint: {'center_x': .85, 'top': .12}
        elevation: 0

    MDFloatingActionButton:
        id: cam_button
        icon: 'camera-outline'
        on_release: root.switch_cam()       
        pos_hint: {'center_x': .85, 'top': .22}
        elevation: 0

    



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
        ScrollView:
            id: mc_scroll_view
            size_hint: (1, None)
            MDList:
                id: mc_box_all
                size_hint_y: None
                height: self.minimum_height
         

<TFScreen>:
    name: 'TF'

    MDBoxLayout:
        orientation: 'vertical'
        adaptive_height: True
        pos_hint: {'top': 1}  # Align to the top
        spacing: dp(10)

        MDTopAppBar:
            title: "QuickMark"
            right_action_items: [["cog-outline", lambda x: app.show_text_input_dialog()]]
            elevation: 0
        ScrollView:
            id: tf_scroll_view
            size_hint: (1, None)
            MDList:
                id: tf_box_all
                size_hint_y: None
                height: self.minimum_height

                
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

            

<OneCheckScreen>
    name: 'onecheck'


    MDStackLayout:
        md_bg_color: (0.95,0.95,0.95,1)
        height: self.minimum_height
        pos_hint: {'center_x': 0.5}
        MDTopAppBar:
            title: "QuickMark"
            right_action_items: [['']]
            left_action_items: [['chevron-left', lambda x: app.screen_manager_func()]]
            elevation: 0
        BoxLayout:
            canvas.before:
                Color:
                    rgba: 0.95,0.95,0.95,1 # Set the background color here
                Rectangle:
                    pos: self.pos
                    size: root.size[0], self.size[1]
            size_hint: (None,None)
            orientation: 'horizontal'
            height: dp(25)
            padding: (20,10)
            size_hint: (0.95,None)

            MDLabel:
                text: "Home > Sheet > Check Papers "
                font_size: dp(10)
                pos_hint: {'center_x':0}

        BoxLayout:
            canvas.before:
                Color:
                    rgba: 1, 1, 1, 1  # Set the background color here
                Rectangle:
                    pos: self.pos
                    size: root.size[0], self.size[1]
            size_hint: (None,None)
            orientation: 'horizontal'
            height: dp(80)
            padding: (20,10)
            size_hint: (0.95,None)
            
            MDTextField:
                md_bg_color: (1,1,1,1)
                icon_left: 'magnify'
                hint_text: "Search..."
                height: dp(20)
                padding: (40, 40)
                size_hint: (0.9,None)
                on_text: root.word_search(*args)

        BoxLayout:
            id: box_label
            canvas.before:
                Color:
                    rgba: 0.95,0.95,0.95,1 # Set the background color here
                Rectangle:
                    pos: self.pos
                    size: root.size[0], dp(1)
            size_hint: (0,None)
            orientation: 'horizontal'
            
            size_hint: (1,None)
            height: 15
            MDLabel:
                id: empty_label
                text: ""
                halign:"center"  # Center the text horizontally
                theme_text_color:"Secondary" # Set the color to gray
                height:5
                pos_hint:{"center_y": 0.5} 
                
        ScrollView:
            id: scroll_view
            size_hint: (1, None)
            height: dp(500)

            MDList:
                id: onecheck_list 
                size_hint_y: None
                height: self.minimum_height
                md_bg_color: (1,1,1,1)
                padding: 0  # Set padding to 0
                spacing: 0 


    MDFloatingActionButton:
        id: plus_button
        icon: 'plus'
        on_release: root.add_new_sheet()        
        pos_hint: {'center_x': .85, 'top': .12}
        elevation: 0


        

    
        
'''

class OneCheckScreen(Screen):
    
    def add_new_sheet(self):
        print("ADDING NEW SESSION")
        check_obj = fs.get_sheet(fs.open_index).check_sheets
        check_obj.add_session()
        check_obj.get_session(-1).name = str(len(check_obj.check_sessions)) # gets last added sheet (index "-1")
        instance_screen = self.manager.get_screen('check')
        check_obj.get_session(-1).name = str(f'STUDENT {len(check_obj.check_sessions)}')
        #fs.save()
        self.add_item_to_list()
        toast("New Checking Session Added.", (1,0,1,0.2), 1)

    def add_item_to_list(self, item_text="New Item Added"):
        check_list = self.ids.onecheck_list
        check_obj = fs.get_sheet(fs.open_index).check_sheets
        sessions = check_obj.check_sessions


        
        if len(sessions) > 0:
            session_last = sessions[-1]
            session_instance = InstanceCheckScreen(text=session_last.name)
            session_instance.select_id = len(sessions)-1 #sheet_i
            session_instance.manager = self.manager
            session_instance.add_widget(IconLeftWidgetWithoutTouch(icon='account-outline'))
            session_instance.add_widget(IconRightWidgetWithoutTouch(icon='chevron-right'))
            session_instance.secondary_text = 'Date Created: '+ str(session_last.date_created).split(' ')[0]
           
            check_list.add_widget(session_instance)
            self.manager.change_screen ('check')
            

        


    def go_to_score_screen(self, instance):
        self.manager.current = 'check'

    




class InstanceCheckScreen(TwoLineAvatarIconListItem):
    def __init__(self, **kwargs):
        super(InstanceCheckScreen, self).__init__(**kwargs)
        self.select_id = None
        self.manager = None
    
    def on_release(self, *args, **kwargs):
        print("GETTING THERE")
        #fs.get_sheet(self.select_id).name = str(fs.get_sheet(self.select_id).name)
        fs.get_sheet(fs.open_index).check_sheets.session_open_index = self.select_id
        self.manager.get_screen('check').start()
        self.manager.change_screen('check')
        

class Instance(TwoLineAvatarIconListItem):
    def __init__(self, **kwargs):
        super(Instance, self).__init__(**kwargs)
        self.select_id = None
        self.manager = None
    
    def on_release(self, *args, **kwargs):
        #fs.get_sheet(self.select_id).name = str(fs.get_sheet(self.select_id).name)
        #name_screen = self.manager.get_screen('name')
        #name_screen.ids.text_field.text = fs.get_sheet(self.select_id).name
        fs.open_index = self.select_id
        self.manager.change_screen('name')
        #self.manager.current = 'name'



class MCInstanceBox(BoxLayout):
    def __init__(self, number, **kwargs):
        super(MCInstanceBox, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        self.spacing = dp(2)
        self.size_hint_x = None
        self.size_hint_y = None
        self.buttons = []
        self.padding = (10,10)
        self.minimum_width = dp(1)
        self.number = number
        self.width = dp(50)
        self.true_answer = fs.sheets[fs.open_index].answer_key.mc.items[self.number].answer_key
        print(self.true_answer)
        # Add label
        

        # Add buttons
        for letter in ['A','B','C','D','None']:
            button = MDFlatButton(text=letter, id=letter)
             # Bind size changes to update_button_size method
            self.add_widget(button)
            
            
            self.buttons.append(button)
            self.toggle_button_state(button,self.true_answer)
            button.bind(on_release=lambda btn=button: self.toggle_button_state(btn))

    def toggle_button_state(self,button, initialize=None):
        # Deselect all buttons
        buttons = self.buttons
        #print(button.text)
        for btn in buttons:
            btn.size_hint = (0.8,1)  # Ensure size_hint is set before width and height
            if btn.text != button.text if initialize is None else btn.text != initialize:
                btn.md_bg_color = [1, 1, 1, 1]  # Revert background color to white
            else:
                btn.md_bg_color = [0.5,0.5,0.5,1]
                fs.sheets[fs.open_index].answer_key.mc.items[self.number].answer_key = [btn.text]
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
        for letter in ['T','F','None']:
            button = MDFlatButton(text=letter, id=letter)
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
                fs.sheets[fs.open_index].answer_key.tf.items[self.number].answer_key = [btn.text]
        
        
        # Highlight the pressed button

  
class HomeScreen(Screen):
    def show_key_button(self):
        pass
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
        saved_list = self.ids.saved_list
        word_keys = []
        obj_content = []
        for subwidget in self.ids.saved_list.children:
            word_keys.append(subwidget.text)
            obj_content.append([subwidget.text,subwidget.secondary_text, subwidget.select_id])
        search_system = SearchSystem(word_keys, obj_content)
        result = search_system.search(text,True)

        for subwidget, widget_detail in zip(self.ids.saved_list.children, result[::-1]):
            subwidget.text = widget_detail[0]
            subwidget.secondary_text = widget_detail[1]
            subwidget.select_id = widget_detail[2]

    def respond_to_rename(self):
        print('responding to rename')
        saved_list = self.ids.saved_list
        for subwidget in saved_list.children:
            
            if subwidget.select_id == fs.open_index:
                print('renaming')
                subwidget.text = fs.sheets[fs.open_index].name
        
    def add_item_to_list(self, defined_sheets=[]):
        """Uodate list

        Args:
            defined_sheets (list, optional): _description_. Defaults to [].
        """
        print("ADDING TO LIST")
        saved_list = self.ids.saved_list
        #saved_list.clear_widgets()
        if len(fs.sheets) == 0:
            self.ids.empty_label.text = 'You have no sheets.\nCreate one by tapping the + button'
            self.ids.box_label.height = 100
        else:
            self.ids.empty_label.text = ''
            self.ids.box_label.height = 5
        # Create an MDLabel
        if len(fs.sheets) > 0:
            if len(defined_sheets) == 0:
                sheet = fs.sheets[-1]
            else:
                sheet = defined_sheets[-1]
            sheet_name = sheet.name
            instance = Instance(text=sheet_name)
            instance.add_widget(IconLeftWidgetWithoutTouch(icon='file-document-outline'))
            instance.add_widget(IconRightWidgetWithoutTouch(icon='chevron-right'))
            instance.select_id = len(fs.sheets)-1 #sheet_i
            fs.open_index = instance.select_id
            instance.manager = self.manager
            instance.secondary_text = 'Date Created: '+ str(sheet.date_created).split(' ')[0]
            saved_list.add_widget(instance)

    def show_init_list(self, defined_sheets=[]):
        """Uodate list

        Args:
            defined_sheets (list, optional): _description_. Defaults to [].
        """
        print("ADDING TO LIST")
        saved_list = self.ids.saved_list
        #saved_list.clear_widgets()
        if len(fs.sheets) == 0:
            self.ids.empty_label.text = 'You have no sheets.\nCreate one by tapping the + button'
            self.ids.box_label.height = 100
        else:
            self.ids.empty_label.text = ''
            self.ids.box_label.height = 5
        # Create an MDLabel
        for ishet in range(len(fs.sheets)):
            if len(defined_sheets) == 0:
                sheet = fs.sheets[ishet]
            else:
                sheet = defined_sheets[-1]
            sheet_name = sheet.name
            instance = Instance(text=sheet_name)
            instance.add_widget(IconLeftWidgetWithoutTouch(icon='file-document-outline'))
            instance.add_widget(IconRightWidgetWithoutTouch(icon='chevron-right'))
            instance.select_id = ishet #sheet_i
            instance.manager = self.manager
            instance.secondary_text = 'Date Created: '+ str(sheet.date_created).split(' ')[0]
            saved_list.add_widget(instance)
        

        layout = BoxLayout(orientation='vertical', padding=20) # Add padding around the layout
        
        label = MDLabel(
            text=f"\n{'.'}\n",
            halign="center",  # Center the text horizontally
            theme_text_color="Secondary",  # Set the color to gray
            size_hint_y=None,
            height=20,  # Adjust the height of the label
            padding=(20, 10) , # Add padding around the label
            pos_hint={"center_y": 0.5}
        )
        #saved_list.add_widget(MDLabel(
         #           text="\n\n",
          #          halign="center",  # Center the text horizontally
           #         theme_text_color="Secondary",  # Set the color to gray
            #        size_hint_y=None,
             #       height=20,  # Adjust the height of the label
              #      padding=(20, 10) , # Add padding around the label
               #     pos_hint={"center_y": 0.5} 
                #))
        #saved_list.add_widget(label)

        
        self.ids.scroll_view.height = Window.height-(240)
        


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


#CLASS____________________________________________________________-
            

class NameScreen(Screen):
    #INIT_________________________________________________________
    def __init__(self, **kwargs):
        super(NameScreen, self).__init__(**kwargs)

    def on_screen(self,*args,**kwargs):
        self.ids.text_field.text = fs.get_sheet(fs.open_index).name

    #METHOD_________________________________________________________
    def prepare_mc_keys(self):
        
        mc_screen = self.manager.get_screen('MC') # set variables to reference to screen attributes
        answer_key = fs.sheets[fs.open_index].answer_key.mc # set variable for reference on file system attribute for ease
        mc_screen.instances = [] # init instances for screen
        #mc_screen.ids.mc_box_all.clear_widgets() # out
        widgets_to_remove = [] # init
    
        # Iterate through the children of tf_box_all; which widgets to remove
        for child in mc_screen.ids.mc_box_all.children:
            # Check if the child is an instance of TopAppBar
            if not isinstance(child, MDTopAppBar): # exclude MDTOPAPP BAR; upd: condition not necessary
                # If it's not a TopAppBar, add it to the list of widgets to be removed
                widgets_to_remove.append(child)
        
        # Remove the widgets from tf_box_all
        for widget in widgets_to_remove:
            mc_screen.ids.mc_box_all.remove_widget(widget)


        bg_color = [(1,1,1,1),(0.5,0.5,0.5,1)] # bg color constant
        increment = 0 # init increment

        # base iteration on the amount of items on answer key
        # dynamic generation of list
        for answer_item in answer_key.get_items():
            label = MDLabel(text=f'{increment+1} ') # number count display
            label.color=(0.5,0.5,0.5,1) # label color

            # add on gui
            mc_screen.ids.mc_box_all.add_widget(label) # add number count display
            instance = MCInstanceBox(increment) # initialize box
            instance.md_bg_color=bg_color[int((increment+1)%2)] # upd: doesnt work; make bg color different per row by odd or even row count
            mc_screen.ids.mc_box_all.add_widget(instance)
            mc_screen.instances.append(instance) # add box to screen

            increment += 1

        # prevent from cutting off items from scroll view
        mc_screen.ids.mc_scroll_view.height = Window.height - (150)
        # debugging
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
            instance.size_hint = (1,None)
            instance.adaptive_width = True
        tf_screen.ids.tf_scroll_view.height = Window.height - (130)
        print(tf_screen.instances)
    
    def prepare_answer_sheet(self):
        """FUNCTION for click event before entering answer sheet. 
        SHow gui on sheet_screen based on registered data from filesystem
        """
        sheet_screen = self.manager.get_screen('answer_sheet')
        answer_key = fs.sheets[fs.open_index].answer_key
        sheet_screen.ids.mcq_textfield.text = str(len(answer_key.mc.get_items()))
        sheet_screen.ids.tf_textfield.text = str(len(answer_key.tf.get_items()))
        sheet_screen.ids.ident_textfield.text = str(len(answer_key.idtf.get_items()))
        sheet_screen.ids.mcq_checkbox.active = True if len(answer_key.mc.get_items()) > 0 else False
        sheet_screen.ids.tf_checkbox.active = True if len(answer_key.tf.get_items()) > 0 else False
        sheet_screen.ids.ident_checkbox.active = True if len(answer_key.idtf.get_items()) > 0 else False

        name = fs.sheets[fs.open_index].name
        sheet_screen.generate_template(len(answer_key.mc.get_items()), len(answer_key.tf.get_items()), len(answer_key.idtf.get_items()), name)


    def rename(self):
        """Renaming Function
        """
        # debugging
        print("RENAMING")

        index = fs.open_index # index for currently opened sheet
        current_name = self.ids.text_field.text # use current name on text field gui
        fs.sheets[index].name = current_name # update filesystem 

        #fs.save() #out; now autosaves
        home_screen = self.manager.get_screen('home')
        home_screen.respond_to_rename()
        
        #home_screen.add_item_to_list()

        # quick confirmation dialog
        toast("Renamed successfully.", (1,0,1,0.2), 1)


    def capitalize(self, instance, text):
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
        pass

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


#CLASS____________________________________________________________

class FileManager(MDFileManager):
    def __init__(self,path_function,starting_path, dir_only=True,**kwargs):
        super(FileManager, self).__init__(**kwargs)
        self.previous_path = starting_path
        self.show_hidden_files=False
        self.ext = ['.????????????????'] if dir_only else []
        self.path_function = path_function

        pass

    def file_manager_open(self):
        # Show file manager starting from the previous selected path or root directory
        
        self.show(self.previous_path)

    def select_path(self, path):
        # Method to handle file selection event
        self.previous_path = path  # Store the selected path
        fs.filemanager_last_dir = path
        self.run_script(path)
        
        self.close()

    def run_script(self, file_path):
        # Method to run a script using the selected file path
        if os.path.isfile(file_path):
            # Example: Run a Python script
            print(f"python {file_path}")
        output, error,destination = self.path_function(file_path)
        if output==True:
            toast(f"Success! Image saved as: \n{destination}.")
        else:
            toast(f"Export failed. {error}")
            

    def exit_manager(self, *args):
        # Method to handle exit event
        
        self.close()
        

# CLASS_________________________________________________________
        

class IDScreen(Screen):
    pass


#CLASS________________________________________________________


class CheckScreen(Screen):

    def on_screen(self):
        print ('Hello World')

    def capitalize_check(self, instance, text):
        instance.text = text.capitalize()  # Capitalize the text in the text field

    def update_sheet_name(self):
        sheet_name = fs.sheets[fs.open_index].name
        self.ids.check_text_field.text = sheet_name
        check_sheet= fs.get_sheet(fs.open_index).check_sheets
        check_session= check_sheet.get_session (check_sheet.session_open_index)
        self.ids.check_text_field= check_session.name

    #METHOD________________________________________________

    
    def cam_off(self):
        """Function for turning camera off
        """
        self.remove_widget(self.camera_widget)
        self.camera_widget.remove_camera = True # attribute from camera widget class; stop looping process on bg when True
        self.camera_widget.camera.remove_from_cache()
        self.camera_widget.camera.play = False # stop camera from playing
        del self.camera_widget.camera._camera
        del self.camera_widget
        self.cam_is_on = False  # status indicator


    #METHOD____________________________________________
    def update(self, test_type):
        value=None
        check_sheet = fs.get_sheet(fs.open_index).check_sheets
        print(check_sheet.session_open_index)
        check_session=check_sheet.get_session(check_sheet.session_open_index)

        if test_type == 'MULTIPLE CHOICE':
            value = check_session._mc_score
            self.ids.mc_indicator.text = f'Multiple Choice: {value}'
            if value is not None:
                self.ids.mc_indicator.color = (0,0.5,0,1)
            print('mc none')
            
        elif test_type == 'TRUE OR FALSE':
            value = check_session._tf_score
            self.ids.tf_indicator.text = f'True or False: {value}'
            if value is not None:
                self.ids.tf_indicator.color = (0,0.5,0,1)
            else:
                print('tf none')
        else:
            value = check_session._idtf_score
            self.ids.idtf_indicator.text = f'Identification: {value}'
            if value is not None:
                self.ids.idtf_indicator.color = (0,0.5,0,1)
            else:
                print('idtf none')

    def cam_on(self):
        """Func for turning camera on
        """

        # reference file system variables for shortening
        mc = fs.sheets[fs.open_index].answer_key.mc
        tf = fs.sheets[fs.open_index].answer_key.tf
        idtf = fs.sheets[fs.open_index].answer_key.idtf

        # renames 'None' string to literal None object
        mc_answers = [x.answer_key if x.answer_key != 'None' else None for x in mc.get_items()]
        tf_answers = [x.answer_key if x.answer_key != 'None' else None for x in tf.get_items()]
        idtf_answers = [x.answer_key for x in idtf.get_items()]

        # debugging
        print(mc,tf,idtf)
        
        #self.camera_widget = CameraWidget() # out
        # pass answer keys to camera widget as ground truth later.
        check_sheet = fs.get_sheet(fs.open_index).check_sheets
        self.camera_widget = CameraWidget(mcq_correct=mc_answers, 
                                          tf_correct=tf_answers,
                                          idtf_correct=idtf_answers,
                                          primary_storage=root_folder,
                                          check_session=check_sheet.get_session(check_sheet.session_open_index),
                                          checkscreen=self)
        self.add_widget(self.camera_widget)


        #
        #
        #
        #
        # Set the position of the camera widget to be at the top of the screen
        self.camera_widget.pos_hint = {'top': .9}

        # status indicator
        self.cam_is_on = True

    def start(self,*args,**kwargs):
        for x in ['MULTIPLE CHOICE', 'TRUE OR FALSE', 'IDENTIFICATION']:
            self.update(x)

    


    #METHOD________________________________________________

    def switch_cam(self,*args,**kwargs):
        """Switching cams based on status indicator
        """
        if self.cam_is_on == False:
            self.cam_on()
        else:
            self.cam_off()
    

    #INIT______________________________________________________
            
    def __init__(self,**kwargs):
        super(CheckScreen, self).__init__(**kwargs)
        self.cam_is_on = False # initialize status indicator

    def add_new_sheet(self):
        print("ADDING NEW SESSION")
        check_obj = fs.get_sheet(fs.open_index).check_sheets
        check_obj.add_session()
        check_obj.get_session(-1).name = f'STUDENT {len(check_obj.check_sessions)}'

        # Get a reference to the OneCheckScreen instance
        one_check_screen = self.manager.get_screen('onecheck')
        
        # Call the method to add item to the list in OneCheckScreen
        one_check_screen.add_item_to_list()

        toast("New Checking Session Added.", (1, 0, 1, 0.2), 1)

    def go_to_score_screen(self, instance):
        self.manager.current = 'check'



    


#CLASS_________________________________________________________

class AnswerSheetScreen(Screen):
    """Screen class for managing answer sheet functionalities.

    Attributes:
        None

    Methods:
        apply_count_for_type(key_type): Applies the count for a specific key type (e.g., mc, tf, idtf).
        apply_count(): Applies the count for all key types (mc, tf, idtf).
        show_text_field(active, checkbox_type): Enables or disables text fields based on checkbox state.
    """
    def __init__(self, **kwargs):
        super(AnswerSheetScreen, self).__init__(**kwargs)
        pass

    #METHOD___________________________________________________
    def share(self):
        Function.copy_file('assets/whole_template.png', fs.filemanager_last_dir+'/'+'temp--QM.png')
        Function.share(os.path.abspath('assets/whole_template.png').replace("\\", "/"))

    #METHOD_____________________________________________________
    def open_file_manager(self, *args):
        sheet_name = fs.sheets[fs.open_index].name
        unique_name = str(datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))
        fm = FileManager(lambda x: Function.copy_file('assets/whole_template.png', x+'/'+sheet_name+f' {unique_name}.png'), fs.filemanager_last_dir).file_manager_open()

    #METHOD_____________________________________________________-

    def apply_count_for_type(self, key_type):
        """Applies the count for a specific key type.

        Args:
            key_type (str): The type of key (mc, tf, idtf).

        Returns:
            None
        """
         #file system obj; get sheet based on opened index (openeded sheet on gui). then get answer keys
        answer_key = fs.sheets[fs.open_index].answer_key
        textfield = None # init
        count = 0 # init

        # set variables based on key type
        if key_type == 'mc':
            answer_key = answer_key.mc
            textfield = self.ids.mcq_textfield
        elif key_type == 'tf':
            answer_key = answer_key.tf
            textfield = self.ids.tf_textfield
        elif key_type == 'idtf':
            answer_key = answer_key.idtf
            textfield = self.ids.ident_textfield

        # if textfield is disabled. Assume 0 count
        if textfield.disabled == True or textfield.text == '':
            count = 0
        else:
            count = int(textfield.text)

        # Debugging
        print(textfield.disabled)
        print(f'{key_type} item count: {count}')
        print('showing', answer_key.show_items)

        answer_key.set_items(count) # setting items using method from FileSystem
        toast("Sheet Updated.")
        return count
    
    #METHOD__________________________________________________
   
    def generate_template(self, mc, tf, idtf, name):
        template_path = stitch_sheet(mc_num=mc,
                     idtf_num=idtf,
                     tf_num=tf,
                     title=name)
        
        image_texture = CoreImage(template_path).texture
        
        # Update the texture of the Image widget
        self.update_image_texture(image_texture,template_path)
        

    def update_image_texture(self, texture,path):
        # Get a reference to the Image widget
        image = self.ids.generated_image
        
        # Temporarily clear the source to force a texture reload
        image.source = ''
        
        # Assign the new texture
        image.texture = texture
        
        # Assign the source again to ensure the update is triggered
        image.source = path
        
        # Trigger a layout update to force the image to redraw
        image.reload()



    #METHOD__________________________________________________
        

    def apply_count(self):
        """Applies the count for all key types (mc, tf, idtf).

        Args:
            None

        Returns:
            None
        """
        mc_count = self.apply_count_for_type('mc')
        tf_count = self.apply_count_for_type('tf')
        idtf_count = self.apply_count_for_type('idtf')
        name = fs.sheets[fs.open_index].name
        self.generate_template(mc_count, tf_count, idtf_count, name)
        

    #METHOD_____________________________________________________


    def show_text_field(self, active, checkbox_type):
        """Enables or disables text fields based on checkbox state.

        Args:
            active (bool): Flag indicating whether the checkbox is active or not.
            checkbox_type (str): The type of checkbox ('mcq', 'tf_textfield', 'ident').

        Returns:
            None
        """
        if checkbox_type == 'mcq':
            self.manager.get_screen('answer_sheet').ids.mcq_textfield.disabled = not active
        elif checkbox_type == 'tf_textfield':
            self.manager.get_screen('answer_sheet').ids.tf_textfield.disabled = not active
        elif checkbox_type == 'ident':
            self.manager.get_screen('answer_sheet').ids.ident_textfield.disabled = not active


#CLASS____________________________________________
            
class MCScreen(Screen):
    pass

#_________________________________________________


def autosave():
    """Autosaves changes on filesystem into permanent local storage.

    TODO: Prevent data corruption while saving

    """
    
    fs.save() # saves filesystem
    autosave_sched() # restart when done


#_______________________________________________


def autosave_sched():
    """Function for scheduler on thread.
    Used to retrigger saving only after previous saving is done.
    """
    Clock.schedule_once(lambda x:threading.Thread(target=lambda: autosave()).start(),0.01) # using kivy scheduler; do thread.


#_________________________________________________
    
        
class CustomScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.transition = NoTransition()
        

    def change_screen(self, screen_name):
        self.current = screen_name
        screen = self.get_screen(screen_name)

        try:
            screen.on_screen()
        except Exception as e:
            print('screen.change_screen():',e)

class App(MDApp):

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Indigo"
        self.screen = Builder.load_string(KV)


        return self.screen   

    #________________________________________________
   

    def on_start(self):
        """on startup initiializations
        """
        home_screen = self.root.get_screen('home')
        #home_screen.add_item_to_list()
        home_screen.show_init_list()
        autosave_sched()
        from kivy.base import EventLoop
        EventLoop.window.bind(on_keyboard=self.hook_keyboard)

    #_____________________________________________________
    
    def screen_manager_func(self):
        dummy = self.root.get_screen('home')  # Just for accessing the manager attribute
        if dummy.manager.current == 'home':  # On the first screen
            self.stop()  # Stop the app
        elif dummy.manager.current == 'name':
            dummy.manager.current = 'home'  # Go back to the home screen
        elif dummy.manager.current == 'onecheck':
            dummy.manager.current = 'name'  # Go back to the name screen when chevron-left button is pressed
        elif dummy.manager.current == 'check':  # Checking/Scanning of sheet
            dummy.manager.current = 'onecheck'  # Switch to the 'onecheck' screen
            try:
                if self.root.get_screen('check').cam_is_on:  # Turn off the camera if it's on
                    self.root.get_screen('check').cam_off()
            except Exception as e:
                print(e)
                pass
        else:  # For other screens not listed, go back to the name screen
            dummy.manager.current = 'name'

    
    #_________________________________________________________

    def hook_keyboard(self, window, key, *largs):
        """Add keyboard event for back or esc
        """
        if key == 27:
            self.screen_manager_func()
            return True 
        
    #__________________________________________________________

    def update_label(self, instance):
        """?..."""
        text_input = instance.text
        display_label = self.root.get_screen('name').ids.display_label
        current_date = datetime.now().strftime('%Y-%m-%d')
        display_label.text = f"{text_input}\n{current_date}"
        text_field = self.root.get_screen('name').ids.text_field
        self.root.get_screen('name').remove_widget(text_field)
        save_button = self.root.get_screen('name').ids.save_button
        self.root.get_screen('name').remove_widget(save_button.parent)

    #____________________________________________________________

    def save_and_display_text(self):
        """?...
        """
        text_input = self.root.get_screen('name').ids.text_field.text
        self.update_label(self.root.get_screen('name').ids.text_field)

        # Add item to the list
        home_screen = self.root.get_screen('home')
        home_screen.add_item_to_list(text_input)

        # Remove save button
        save_button = self.root.get_screen('name').ids.save_button
        self.root.get_screen('name').remove_widget(save_button.parent)


class Function:
    def copy_file(source_path, destination_path):
        """
        Copy a file from the source path to the destination path.

        Args:
        - source_path (str): The path of the source file.
        - destination_path (str): The path where the file will be copied.

        Returns:
        - bool: True if the file was successfully copied, False otherwise.
        """
        try:
            # Copy the file
            shutil.copy(source_path, destination_path)
            return True, '', destination_path
        except Exception as e:
            print(f"An error occurred: {e}")
            return False, str(e), destination_path
        
    def share(path):
        try:
            from android.storage import primary_external_storage_path
            from jnius import autoclass
            from jnius import cast
            import os
            
            StrictMode = autoclass('android.os.StrictMode')
            StrictMode.disableDeathOnFileUriExposure()
            
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            
            Intent = autoclass('android.content.Intent')
            String = autoclass('java.lang.String')
            Uri = autoclass('android.net.Uri')
            File = autoclass('java.io.File')

            shareIntent = Intent(Intent.ACTION_SEND)
            shareIntent.setType('image/png')
            path = fs.filemanager_last_dir+'/'+'temp--QM.png'
            imageFile = File(path)
            uri = Uri.fromFile(imageFile)
            parcelable = cast('android.os.Parcelable', uri)
            shareIntent.putExtra(Intent.EXTRA_STREAM, parcelable)
            #shareIntent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
            #shareIntent.addFlags(Intent.FLAG_GRANT_WRITE_URI_PERMISSION)
            currentActivity = cast('android.app.Activity', PythonActivity.mActivity)
            currentActivity.startActivity(shareIntent)

            #________________________________________
            
        except Exception as e:
            toast(str(e))

#START OF SCRIPT___________________________________________________

if on_android:
    root_folder = android_storage
else:
    root_folder = os.getcwd()

# load filesystem previous data from permanent local storage;
# comment out to not use previous data (warning; overwrites with empty new data because of autosave on app run)
try:
    fs = FileSystem()
    fs = fs.load() 

except Exception as e:
    fs = FileSystem()
    pass

try:
    if fs.filemanager_last_dir is None:
        fs.filemanager_last_dir = root_folder
except Exception as e:
    print(e)


App().run() # RUN APP; init