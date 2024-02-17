from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.boxlayout import MDBoxLayout
####
from screens.first import FirstScreen
from screens.second import SheetScreen
from screens import first, second

class TestApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Purple"
        self.first_screen = FirstScreen(name='first')
        self.sheet_screen = SheetScreen(name = 'second')
        self.screen_manager = ScreenManager(transition=NoTransition())
        first.screenmanager = self.change_screen
        second.screenmanager = self.change_screen
        self.screen_manager.add_widget(self.first_screen)
        self.screen_manager.add_widget(self.sheet_screen)
        return self.screen_manager
    
    def change_screen(self, name):
        self.screen_manager.current = name

TestApp().run()

