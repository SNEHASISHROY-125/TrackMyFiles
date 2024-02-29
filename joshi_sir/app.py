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

# Results-add
from kivymd.uix.textfield import MDTextField

from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.list import OneLineListItem
from kivymd.uix.button import MDIconButton
from kivymd.uix.label import MDLabel
from kivy.clock import Clock

# db_func
import db as db

# exception handling
import sys

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
        BoxLayout:
            orientation: 'vertical'

            MDTopAppBar:
                title: "Search Results"
                left_action_items: [['home', lambda x: app.to_home()]]
                
                right_action_items: [['magnify', lambda x: app.show_search_dialog()]]

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
        # exception handling in kivy | call my_exception_hook
        sys.excepthook = self.my_exception_hook
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
        # 
        text_field_text = self.root.get_screen('main').children[0].children[0].children[2].text
        # db_payload['file_dir'] = self.path
        
        # add to db 
        # check if db_payload is not empty:
        if text_field_text == 'name your memo' or text_field_text== '' or text_field_text == 'memo': toast('Please enter a memo')
        else:
            # add to db_payload
            db_payload['memo'] = text_field_text
            self.add_to_db()
        

    ''' Add to db '''
    def add_to_db(self):
        global db_payload
        # add to db:
        db.insert_data(db_payload['date'], db_payload['file_dir'], db_payload['memo'])
        # set to default text: ...
        self.root.get_screen('main').children[0].children[0].children[2].text = 'name your memo'
        
        # toast sucess message
        toast('Memo added successfully')

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
        # serach-dialog-box content-API
        search_query = self.dialog.content_cls.text
        print(f'Searching for: {search_query}')
        # search in db...
        t_ = db.query_db(search_query)
        # print(t_)
        # clear the results screen first:
        self.delete_widget(None)
        # add result to results screen:
        # self.add_result([self.dialog.content_cls.text])
        self.add_result(t_)
        self.dialog.dismiss()
        # change screen to results
        self.root.current = 'results'

    ''' search end '''

    def my_exception_hook(self, *args):
        # close the db connection
        db.close_db_connection()
        print('db connection closed')
    def on_start(self):...
    def on_stop(self):
        # close the db connection
        db.close_db_connection()
        print('db connection closed')
    
    ''' add result | S2 '''
    def add_result(self,content:list=['search result']):
        # 
        global results_widget_list
        #
        # item = OneLineAvatarIconListItem(text=f'result:{content}')
        # icon_btn = MDIconButton(icon="android")
        # icon_btn.bind(on_release=self.delete_widget)
        # item.children[0].add_widget(icon_btn)
        def add_content(content:tuple):
            result_text = content[-1] # content
            result_url = content[-2] # url {file-dir}
            print('result_text:', result_text, 'result_url:', result_url)
            item = OneLineListItem()
            box = item.children[0]
            box.orientation = 'horizontal'
            box.spacing = 70
            # box = BoxLayout(orientation='horizontal', spacing=10)
            icon_btn = MDIconButton(icon="close-circle", size_hint_x=None, width=50)
            open_btn = MDIconButton(icon="open-in-new", size_hint_x=None, width=50)
            open_btn.bind(on_release=lambda x: toast('explorer {}'.format(result_url)))
            open_btn.bind(on_release=lambda x: self.open_dir(result_url))
            label = MDTextField(
                    text=result_text,
                )
            box.add_widget(icon_btn)
            box.add_widget(label)
            box.add_widget(open_btn)
            # item.add_widget(box)
            # add the widget to list to remove or do something in future
            results_widget_list.append(item)
            #
            # print('root is :', self.root.get_screen('results').children[0].children[0].children[0])
            # print(item.children[0])
            self.root.get_screen('results').children[0].children[0].children[0].add_widget(item)
            # self.root.get_screen("results").ids.container.add_widget(item)
        for i in content:  # 1 * i -> delay_sec
            print('DD: ',i)
            # self.root.get_screen('results').children[0].children[0].children[0].add_widget(OneLineListItem(text=i[-1]))
            add_content(i)
            # Clock.schedule_once(lambda dt: add_content(i), 1 * 0.3)

    def delete_widget(self, r):
            global results_widget_list
            root = self.root.ids.container
            [root.remove_widget(w) for w in results_widget_list]
    
    ''' add result end '''

    ''' open file explorer '''
    def open_dir(self,dir_path:str):
        try:
            subprocess.Popen('explorer {}'.format(dir_path), shell=True)
        except Exception as e: toast('Error: {}'.format(e))
    ''' home '''
    def to_home(self):
        self.root.current = 'main'
        # remove all widgets from results screen
        # self.delete_widget(None)
    ''' home end '''

    ''' results-screen '''
    def to_history(self):
        self.root.current = 'results'


# memry_dict
# db_payload to insert into db
global db_payload
db_payload = {
    'date': get_date(),
    'file_dir': 'C:/Users/Snehasish/Downloads/telegram_bot',
    'memo': 'telegram'
}

# widget_list of widgets that are added in after search results-screen
# add or delete widgets from {results} main widget tree
global results_widget_list
results_widget_list = []




Example().run()