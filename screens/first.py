# kivymd essentials
from kivy.metrics import dp
# kivymd uix
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField

from kivy.graphics import Color, RoundedRectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.modalview import ModalView
from kivymd.uix.button import MDRaisedButton

screenmanager = None

class TopToolbar(MDTopAppBar):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = 'QuickMark'
        self.elevation = 0
        self.md_bg_color = tuple([x/256 for x in [160, 111, 189]])
        self.right_action_items = [["plus", lambda x: CreationModal().open()],["dots-vertical", lambda x: None]]

class CreationModal(ModalView):
    class NameField(MDTextField):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.hint_text = 'Sheet Name'
            self.mode = 'fill'
            
            self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (0.8, None)
        self.height = 200
        
        modal_content = BoxLayout(orientation='vertical', padding=dp(20),spacing=dp(10))
        btn_close_modal = MDRaisedButton(text='Create', size_hint=(None, None), elevation=1,size=(200, 50),pos_hint={'center_x': 0.5, 'center_y': 0.5},md_bg_color=tuple([x/256 for x in [160, 111, 189]]))
        btn_close_modal.bind(on_release=self.proceed_create)
        btn_close_modal_cancel = MDRaisedButton(text='Cancel', size_hint=(None, None), elevation=1,size=(200, 50),pos_hint={'center_x': 0.5, 'center_y': 0.5},md_bg_color=(1,1,1,1),text_color=(0,0,0,1))
        btn_close_modal_cancel.bind(on_release=self.dismiss)
        
        modal_content.add_widget(CreationModal.NameField())
        modal_content.add_widget(btn_close_modal)
        modal_content.add_widget(btn_close_modal_cancel)
        
        self.add_widget(modal_content)

        # Set background color using Canvas
        with modal_content.canvas.before:
            Color(1, 1, 1, 1)  # White color
            self.rect = RoundedRectangle(size=modal_content.size, pos=modal_content.pos)

        # Bind size and pos properties to update the background color
        modal_content.bind(size=self.update_rect, pos=self.update_rect)

    def update_rect(self, instance, value):
        # Update the size and position of the rectangle to match the content
        self.rect.size = instance.size
        self.rect.pos = instance.pos

    def proceed_create(self, *args):
        print(screenmanager("second"))
        self.dismiss()
    
class FirstScreen_Layout(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical' 
        self.add_widget(TopToolbar())
        self.add_widget(MDLabel("")) # 
        
class FirstScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(FirstScreen_Layout())
        self.manager = None