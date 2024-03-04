'''

'''

import shutil
import os, datetime

def copy_and_rename(src_path='', dst_dir='', new_name='') -> None:
    """
    Copy a file from the source path to the destination directory and rename it.

    Args:
        src_path (str): The path of the source file.
        dst_dir (str): The path of the destination directory.
        new_name (str): The new name for the copied file.

    Returns:
        None
    """

    if not src_path or not dst_dir:
        # raise ValueError("The source path is required.")
        return

    # Ensure the destination directory exists
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)

    #
    if not new_name: new_name = str(datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S") + ".db")

    # Construct the destination path
    dst_path = os.path.join(dst_dir, new_name)

    # Copy and rename the file
    shutil.copy2(src_path, dst_path)

import tkinter as tk
from tkinter import filedialog

def select_file(title_:str=""):
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(title=title_,filetypes=[("Database files", "*.db")]  # Only allow .db files
    )  # Open the file dialog
    return file_path

def select_directory() -> str:
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    dir_path = filedialog.askdirectory()  # Open the directory dialog
    return dir_path

''' backup-exmport '''
def export_db(source:str,dst_path:str='') -> str:
    # select backup file to import
    if not dst_path:
        dst_path = select_directory()
    # do backup:
    copy_and_rename(dst_dir=dst_path, src_path=source)
    return dst_path

def import_db(source:str) -> None:
    ...


# Usage
# file_path = select_file()
# print(file_path)

# Usage
# copy_and_rename(r"C:\Users\Snehasish\Documents\AAI\win_exe\app_data\my_database.db", r'C:\Users\Snehasish\Downloads\a_new', )

# from kivy.lang import Builder
# from kivymd.app import MDApp

KV = '''
ScrollView:
    do_scroll_x: False
    MDBoxLayout:
        orientation: 'vertical'
        size_hint_y: None
        height: self.minimum_height
        padding: dp(10)
        spacing: dp(10)
        MDCard:
            size_hint: 0.8, None
            height: "180dp"
            pos_hint: {"center_x": .5}
            BoxLayout:
                MDLabel:
                    text: 'Card 1'
                MDIconButton:
                    icon: "language-python"
                    user_font_size: "48sp"
        MDCard:
            size_hint: 0.8, None
            height: "180dp"
            pos_hint: {"center_x": .5}
            BoxLayout:
                MDLabel:
                    text: 'Card 2'
                MDIconButton:
                    icon: "language-python"
                    user_font_size: "48sp"
'''

# # MainApp().run()
# class MainApp(MDApp):
#     def build(self):
#         self.theme_cls.theme_style = "Dark"
#         return Builder.load_string(KV)

# MainApp().run()