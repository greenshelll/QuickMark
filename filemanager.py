from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.filemanager import MDFileManager
import os

KV = '''
BoxLayout:
    orientation: "vertical"

    MDRaisedButton:
        text: "Open File Manager"
        on_release: app.file_manager_open()

    Label:
        id: selected_file_label
        text: "Selected file: None"
'''

class MyApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
        )
        self.previous_path = None  # Initialize previous selected path to None

    def build(self):
        return Builder.load_string(KV)

    def file_manager_open(self):
        # Show file manager starting from the previous selected path or root directory
        starting_path = self.previous_path or '/'
        self.file_manager.show(starting_path)

    def select_path(self, path):
        # Method to handle file selection event
        self.root.ids.selected_file_label.text = f"Selected file: {path}"
        self.previous_path = path  # Store the selected path
        self.run_script(path)
        self.file_manager.close()

    def run_script(self, file_path):
        # Method to run a script using the selected file path
        if os.path.isfile(file_path):
            # Example: Run a Python script
            os.system(f"python {file_path}")

    def exit_manager(self, *args):
        # Method to handle exit event
        self.file_manager.close()

MyApp().run()
