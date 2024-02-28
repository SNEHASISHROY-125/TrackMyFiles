'''

'''

from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.filemanager import MDFileManager
from kivymd.toast import toast
import os
import subprocess 
from kivymd.uix.dialog import MDDialog
# import get_date as gd

from datetime import date
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
# from kivymd.uix.textfield import MDTextField

def get_date() -> str:
    '''
    Returns the current date in the format: "YYYY-MM-DD".
    '''
    return str(date.today())


KV = '''

BoxLayout:
    orientation: 'vertical'

    MDTopAppBar:
        title: "ADD MEMOS"
        left_action_items: [['menu', lambda x: None]]
        right_action_items: [['magnify', lambda x: None]]
        right_action_items: [['magnify', lambda x: app.show_search_dialog()]]


    FloatLayout:
        MDTextField:
            id: text_field
            hint_text: "Name your memo"
            pos_hint: {'center_x': .5, 'center_y': .7}
            size_hint_x: .8
            text: 'memo'
            
        MDIconButton:
            icon: "folder-file"
            theme_text_color: "Custom"
            text_color: get_color_from_hex("#FF0000")
            user_font_size: "70sp"
            pos_hint: {'center_x': .3, 'center_y': .6}
            on_release: app.file_manager_open()
        MDIconButton:
            icon: "check"
            theme_text_color: "Custom"
            text_color: get_color_from_hex("#FF0000")
            pos_hint: {'center_x': .7, 'center_y': .6}
            on_release: app.check()
        
'''


class Example(MDApp):

    dialog = None # for search dialog

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
        )

    def build(self):
        return Builder.load_string(KV)

    def file_manager_open(self):
        self.file_manager.show(
            os.path.expanduser("~"))  # output manager to the screen
        self.manager_open = True

    def select_path(self, path):
        '''It will be called when you click on the file name
        or the catalog selection button.

        :type path: str;
        :param path: path to the selected directory or file;
        '''

        self.exit_manager()
        # add file_dir to db_payload
        db_payload['file_dir'] = path
        toast(path)

    def exit_manager(self, *args):
        '''Called when the user reaches the root of the directory tree.'''

        self.manager_open = False
        self.file_manager.close()
    
    def check(self):
        toast(_:=str(self.root.children[0].children[2].text))
        print(_)
        # add to db_payload
        db_payload['memo'] = _
        # db_payload['file_dir'] = self.path
        
        # add to db 
        print(db_payload)

    '''  Seach   '''
    def show_search_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title='Search',
                type="custom",
                content_cls=MDTextField(
                    hint_text="Enter your search query",
                ),
                buttons=[
                    MDFlatButton(
                        text='CANCEL',
                        on_release=self.close_dialog
                    ),
                    MDFlatButton(
                        text='SEARCH',
                        on_release=self.do_search
                    )
                ],
            )
        self.dialog.open()

    def close_dialog(self, obj):
        self.dialog.dismiss()

    def do_search(self, obj):
        search_query = self.dialog.content_cls.text
        print(f'Searching for: {search_query}')
        self.dialog.dismiss()

    ''' search end '''

    def on_stop(self):...
    def on_start(self):
        pass


# memry_dict
global db_payload
db_payload = {
    'date': get_date(),
    'file_dir': 'C:/Users/Snehasish/Downloads/telegram_bot',
    'memo': 'telegram'
}


Example().run()