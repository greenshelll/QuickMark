import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from helloworld.utility import update_style, get_propsize
from toga.paths import Paths
from toga.hardware import camera
import pickle
import datetime
num = 0



class SheetMenuScreen:
    class layout:
        def __init__(self, widget):
            self.widget = widget

        def add(self,*args):
            self.widget.add(*args)
            return self.widget
        
    class styles:
        btn = Pack(height=50, 
                   width=200)
        btn_container = Pack(padding=10)
        row1 = Pack(flex=0.5)
        main_box = Pack(direction='column', 
                        padding=20, 
                        flex=1)
        row3 = Pack(alignment='center', 
                    flex=1, 
                    direction='column', 
                    padding=20)
        row2 = Pack(alignment='center', 
                    flex=0.8, 
                    direction='column', 
                    padding=20)
        row3_title = Pack(alignment='center', 
                          text_align='center')
        row1_right = Pack(flex=1)
        row1_left = Pack(padding=20, 
                         direction='column',
                        flex=1)
        sheetdate = Pack(font_size=15, 
                         background_color = "#0fffff")
        sheetname = Pack(font_size=20, height=50, width=200)

    def lose_focus(self, handler):
        if self.sheetname.readonly:
            self.sheetname.readonly = False
            self.sheet_edit_btn.text = 'Save'
        else:
            self.sheetname.readonly = True
            self.sheet_edit_btn.text = 'Edit'

        print(Paths().data)
        print(self.sheetname.readonly)

    def gain_focus(self, handler):
        handler.readonly = False
        print(handler.readonly)

    def __init__(self, main_window):
        self.idtf_btn = toga.Button(text="Identification", style=self.styles.btn)
        self.tf_btn = toga.Button(text="True or False", style=self.styles.btn)
        self.mc_btn = toga.Button(text="Multiple Choice", style=self.styles.btn)
        self.checksheet_btn = toga.Button(text="Check Sheets", style=self.styles.btn)
        self.analysis_btn = toga.Button(text='Analysis', style=self.styles.btn)
        self.sheetdate = toga.Label(text="date", style=self.styles.sheetdate)
        self.sheetname_enabled = toga.TextInput(placeholder='Sheet Name',
                                        value='Untitled',
                                        style=self.styles.sheetname,
                                        on_change=lambda x: print('one'),
                                        on_gain_focus=lambda x: print('two'),
                                        on_confirm=lambda x: print('three'),
                                        on_lose_focus=lambda x: print(x.value),
                                        readonly=True)
        
        self.sheetname_box = toga.Box()
        self.sheetname = toga.TextInput(placeholder='Sheet Name',
                                        value='Untitled',
                                        style=self.styles.sheetname,
                                        on_change=lambda x: print('one'),
                                        on_gain_focus=lambda x: print('two'),
                                        on_confirm=lambda x: print('three'),
                                        on_lose_focus=lambda x: print(x.value),

                                        readonly=True)
        self.sheet_edit_btn = toga.Button(text='Edit', on_press=self.lose_focus, style=Pack(flex=1, height=50,background_color='#ffffff'))
        self.row1_right = toga.Box(style=self.styles.row1_right)
        self.row1_left = toga.Box(style=self.styles.row1_left)
        self.row3_title = toga.Label(text="Edit Answer Key", style=self.styles.row3_title)
        self.row3 = toga.Box(style=self.styles.row3)
        self.divider = toga.Divider()
        self.divider2 = toga.Divider()
        self.row2_title = toga.Label(text='Appraisal', style=self.styles.row3_title)
        self.row2 = toga.Box(style=self.styles.row2)
        self.row1 = toga.Box(style=self.styles.row1)
        self.main_box = toga.Box(style=self.styles.main_box)

        self.mc_box, self.tf_box, self.idtf_box, self.checksheet_box, self.analysis_box = (toga.Box(style=self.styles.btn_container) for x in range(5))
        

        self.layout(self.main_box).add(
            self.layout(self.row1).add(
                self.layout(self.row1_left).add(
                    self.layout(self.sheetname_box).add(
                        self.sheetname,
                        self.sheet_edit_btn,
                        
                        
                    ),
                    self.sheetdate
                ),
                self.row1_right
            ),
            self.divider2,
            self.layout(self.row2).add(
                self.row2_title,
                self.layout(self.checksheet_box).add(
                    self.checksheet_btn
                ),
                self.layout(self.analysis_box).add(
                    self.analysis_btn
                )
            ),
            self.divider,
            self.layout(self.row3).add(
                self.row3_title,
                self.layout(self.mc_box).add(
                    self.mc_btn
                ),
                self.layout(self.tf_box).add(
                    self.tf_btn
                ),
                self.layout(self.idtf_box).add(
                    self.idtf_btn
                )
            )
        )
        
class Home:
    class layout:
        def __init__(self, widget):
            self.widget = widget

        def add(self,*args):
            self.widget.add(*args)
            return self.widget
        
    class styles:
        btn = Pack(height=50, 
                   width=200)
        btn_container = Pack(padding=10)
        row1 = Pack(flex=0.5)
        main_box = Pack(direction='column', 
                        padding=20, 
                        flex=1)
        row3 = Pack(alignment='center', 
                    flex=1, 
                    direction='column', 
                    padding=20)
        row2 = Pack(alignment='center', 
                    flex=0.8, 
                    direction='column', 
                    padding=20)
        row3_title = Pack(alignment='center', 
                          text_align='center')
        row1_right = Pack(flex=1)
        row1_left = Pack(padding=20, 
                         direction='column',
                        flex=1)
        sheetdate = Pack(font_size=15, 
                         background_color = "#0fffff")
        sheetname = Pack(font_size=20, height=50, width=200)
    
    def add_sheet(self, *args):
        # Get the current date and time and format it as a string
        formatted_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.main.record[formatted_datetime] = {'name':'Untitled'}
        print(self.main.root_dir)
        self.main.update_record()
        print(self.main.record)
        self.to_SheetMenuScreen()
    def to_SheetMenuScreen(self, *args):
        self.main.main_window.content = self.main.sheet_menuscreen.main_box
    
    def __init__(self, main):
        self.main_scroll = toga.ScrollContainer(horizontal = False, vertical = True)
        self.main = main
        self.plus = toga.Command(action=self.add_sheet,text="add",)
        self.main.main_window.toolbar.add(self.plus)

class Main(toga.App):
    def update_record(self):
        with open(f'{self.root_dir}\\sheets.pkl', 'wb') as file:
            pickle.dump(self.record, file)
    def sample(self, *args):
        print(args)
        print('hello world')
    def back_condition(self,*args):
        if self.main_window.content == self.sheet_menuscreen.main_box:
            self.main_window.content = self.home.main_scroll
        elif self.main_window.content == self.home.main_scroll:
            self.exit()

    def startup(self):
        self.main_window = toga.MainWindow(title="Title")
        self.home = Home(self)
        self.sheet_menuscreen = SheetMenuScreen(self)
        print(self.sheet_menuscreen.main_box)
        self.main_window.content = self.home.main_scroll
        self.root_dir = self.paths.data
        try:
            with open(f'{self.root_dir}\\sheets.pkl', 'rb') as f:
                # Load the object from the file
                self.record = pickle.load(f)
        except FileNotFoundError as e:
            # Open the file in binary write mode and dump the empty list
            with open(f'{self.root_dir}\\sheets.pkl', 'wb') as file:
                pickle.dump([], file)
            with open(f'{self.root_dir}\\sheets.pkl', 'rb') as f:
                # Load the object from the file
                self.record = pickle.load(f)
        print(self.record)
        self.record = {}
        self.update_record()
        self.main_window.show()
        """print("PERMSSION",camera.Camera(self).request_permission())
        print(camera.Camera(self).has_permission)
        async def time_for_a_selfie(self, widget, **kwargs):
            photo = await self.main.camera.take_photo(self.main.camera.devices[1])
        print(self.camera.devices)"""
        



        #self.on_exit(self.back_condition)

        
        

def main():
    return Main()
