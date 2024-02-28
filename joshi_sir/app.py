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

# Screen:
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.transition import MDSwapTransition, MDFadeSlideTransition, MDSlideTransition

# MDList
from kivymd.uix.list import OneLineAvatarIconListItem
from kivymd.uix.button import MDIconButton

def get_date() -> str:
    '''
    Returns the current date in the format: "YYYY-MM-DD".
    '''
    return str(date.today())


KV = '''
MDScreenManager:
    id: smanager

    MDScreen:
        id: mainS
        name: "main"

        BoxLayout:
            orientation: 'vertical'

            MDTopAppBar:
                title: "ADD MEMOS"
                left_action_items: [['menu', lambda x: app.theme_dark()]]
                
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

    MDScreen:
        id: S2
        name: "results"
        ScrollView:
            MDList:
                id: container
        
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
    
    ''' theme '''
    def theme_dark(self):
        # dark theme
        self.theme_cls.theme_style = "Dark"
    def theme_light(self):
        # light theme
        self.theme_cls.theme_style = "Light"

    ''' theme-end '''

    ''' file manager '''
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

    ''' file manager-end '''
    
    def check(self): # .children.__len__()
        toast(_:=str(self.root.get_screen('main').children[0].children[0].children[2].text))
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
        # search in db
        self.add_result()
        self.dialog.dismiss()
        self.root.current = 'results'

    ''' search end '''

    def on_stop(self):...
    def on_start(self):...
    
    ''' add result | S2 '''
    def add_result(self):
        item = OneLineAvatarIconListItem(text=f'Item first, 8')
        icon_btn = MDIconButton(icon="android")
        icon_btn.bind(on_release=self.delete_widget)
        item.children[0].add_widget(icon_btn)
        self.root.get_screen('results').children[0].children[0].add_widget(item)
        # self.root.get_screen("results").ids.container.add_widget(item)

    def delete_widget(self, r):
            global widget_list
            root = self.root.ids.container
            [root.remove_widget(w) for w in widget_list]
    
    ''' add result end '''


# memry_dict
global db_payload
db_payload = {
    'date': get_date(),
    'file_dir': 'C:/Users/Snehasish/Downloads/telegram_bot',
    'memo': 'telegram'
}


Example().run()