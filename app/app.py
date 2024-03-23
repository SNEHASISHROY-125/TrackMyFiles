'''

'''
from kivy.config import Config

# Set the window size
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '600')

# Make the window non-resizable
Config.set('graphics', 'resizable', '0')

# Don't forget to import and run your app after setting the configuration
# from kivy.app import App
# ... rest of your app code ...

#

# import time
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.filemanager import MDFileManager
from kivymd.toast import toast
import os
import subprocess 
from kivymd.uix.dialog import MDDialog
# import get_date as gd

from datetime import datetime
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

# navigation drawer
from kivymd.uix.navigationdrawer import MDNavigationDrawer

# navigation drawer
from kivymd.uix.navigationdrawer import MDNavigationDrawer

# db_func
import db as db # do not call directly | use db.init() to initialize the db & set the db_path before calling any db functions

# explorer
import explorer as ex

# exception handling
import sys
import threading
from pathlib import Path

# sync_db
import sync_db as sync

# import config
import config as cfg

# https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def get_date() -> str:
    '''
    Returns the current date in the format: "YYYY-MM-DD".
    '''
    return str(datetime.now())



KV = '''
<TooltipMDIconButton@MDIconButton+MDTooltip>

MDScreenManager:
    id: smanager

    MDScreen:
        id: mainS
        name: "main"

        MDNavigationDrawer:
            id: nav_drawer

            FloatLayout:
                MDIconButton:
                    icon: 'theme-light-dark'
                    user_font_size: "70sp"
                    pos_hint: {'center_x': .1, 'center_y': .8}
                    on_release: app.change_theme()
                MDIconButton:
                    icon: 'cog'
                    user_font_size: "70sp"
                    pos_hint: {'center_x': .1, 'center_y': .6}
                    on_release: app.to_settings()
                MDIconButton:
                    icon: 'file-pdf-box'
                    user_font_size: "70sp"
                    pos_hint: {'center_x': .1, 'center_y': .4}
                    on_release: app.to_merger()
        BoxLayout:
            orientation: 'vertical'

            MDTopAppBar:
                title: "ADD MEMOS"
                left_action_items: [['menu', lambda x: app.root.ids.nav_drawer.set_state("open") if app.root.ids.nav_drawer.state == "close" else app.root.ids.nav_drawer.set_state("close")]]
                left_action_items: [['menu', lambda x: app.root.ids.nav_drawer.set_state("open") if app.root.ids.nav_drawer.state == "close" else app.root.ids.nav_drawer.set_state("close")]]
                right_action_items: [['magnify', lambda x: app.show_search_dialog()]]


            FloatLayout:
                MDTextField:
                    id: text_field
                    hint_text: "Name your memo"
                    pos_hint: {'center_x': .5, 'center_y': .8}
                    size_hint_x: .8
                    text: 'memo'
                    max_text_length: int(app.config_tree_['app']['memo_text_limit'])
                    on_text_validate: app.file_manager_open()
                    
                MDTextField:
                    id: text_field_folder
                    hint_text: "C:/"
                    pos_hint: {'center_x': .5, 'center_y': .7}
                    size_hint_x: .8
                    icon_right: "folder"
                    text: 'C:/Users/sample/Downloads/sample.jpg'
                    required: True
                    helper_text: "Select a folder or file to add memo to."
                    helper_text_mode: "on_error"
                    on_text_validate: app.check()
                    
                MDIconButton:
                    icon: "folder"
                    theme_text_color: "Custom"
                    text_color: app.theme_cls.primary_color
                    user_font_size: "70sp"
                    pos_hint: {'center_x': .87, 'center_y': .72}
                    on_release: app.file_manager_open()

                MDIconButton:
                    icon: "check"
                    theme_text_color: "Custom"
                    text_color: app.theme_cls.primary_color
                    pos_hint: {'center_x': .8, 'center_y': .6}
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
        
    MDScreen:
        id: S3
        name: "settings"
        BoxLayout:
            orientation: 'vertical'

            MDTopAppBar:
                title: "App Settings"
                left_action_items: [['home', lambda x: app.to_home()]]
                right_action_items: [['cloud-upload', lambda x: app.backup()]]
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
                        height: "90dp"
                        pos_hint: {"center_x": .5}
                        BoxLayout:
                            padding: dp(10)
                            MDTextField:
                                id: memo_limit
                                hint_text: "memo text (max) limit"
                                text: str(app.config_tree_['app']['memo_text_limit'])
                            TooltipMDIconButton:
                                tooltip_text: "Change limit"
                                tooltip_bg_color: app.theme_cls.primary_color
                                icon: "pencil"
                                user_font_size: "48sp"
                                on_release: 
                                    app.test('Memo text limit changed to {}'.format(memo_limit.text))
                                    app.config_tree_['app']['memo_text_limit'] = int(memo_limit.text)
                                    app.cfg_.edit_config()

                    MDCard:
                        size_hint: 0.8, None
                        height: "90dp"
                        pos_hint: {"center_x": .5}
                        BoxLayout:
                            padding: dp(10)
                            MDTextField:
                                hint_text: "Current Backup Path in use"
                                text: app.config_tree_['database']['backup_dir']
                            TooltipMDIconButton:
                                tooltip_text: "Select a backup directory"
                                tooltip_bg_color: app.theme_cls.primary_color
                                id: backup_dir
                                icon: "pencil"
                                user_font_size: "48sp"
                                on_release: app.select_backup_dir()
                    MDCard:
                        size_hint: 0.8, None
                        height: "90dp"
                        pos_hint: {"center_x": .5}
                        BoxLayout:
                            padding: dp(10)
                        
                            MDTextField:
                                id: db_restore
                                hint_text: "Current DB in use"
                                text: app.config_tree_['database']['path']
                            TooltipMDIconButton:
                                tooltip_text: "Restore a backup"
                                tooltip_bg_color: app.theme_cls.primary_color
                                id: backup_dir
                                icon: "pencil"
                                user_font_size: "48sp"
                                on_release: app.restore()

    MDScreen:
        id: S2
        name: "merger"
        BoxLayout:
            orientation: 'vertical'

            MDTopAppBar:
                title: "Search Results"
                left_action_items: [['home', lambda x: app.to_home()]]
                
                right_action_items: [['help-circle', lambda x: app.show_anim()]]

            Image:
                source: "./assets/pdf.png"
                anim_delay: 0.03
            MDSpinner:
                palette:
                    [0.28627450980392155, 0.8431372549019608, 0.596078431372549, 1],             [0.3568627450980392, 0.3215686274509804, 0.8666666666666667, 1],             [0.8862745098039215, 0.36470588235294116, 0.592156862745098, 1],             [0.8784313725490196, 0.9058823529411765, 0.40784313725490196, 1],
                size_hint: None, None
                size: dp(46), dp(46)
                pos_hint: {'center_x': .5, 'center_y': .5}
                active: False
            MDRaisedButton:
                text: "Merge PDFs"
                pos_hint: {'center_x': .5, 'center_y': .5}
                on_release: app.merge_pdfs()

'''

#
from kivy.core.window import Window

class TrackMyFiles(MDApp):

    cfg_ = cfg # for kv-string only
    dialog = None # for search dialog
    f_path = None # for file path
    config_tree_ = cfg.config_tree_
    '''for widgets in declarative'''
    # active = False
    # init db
    # setting db_path from config:
    db.db_path = cfg.config_tree_['database']['path']
    db.init()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
        )

    def build(self):
        # exception handling in kivy | call my_exception_hook
        # sys.excepthook = self.my_exception_hook
        # set the icon
        self.icon ='./assets/icon.ico' 
        self.theme_cls.primary_palette = "DeepPurple"
        self.theme_cls.theme_style = cfg.config_tree_['theme']['theme_style']
        print('theme:',cfg.config_tree_['theme']['theme_style'])
        # ['Red', 'Pink', 'Purple', 'DeepPurple', 'Indigo', 'Blue', 'LightBlue', 'Cyan', 'Teal', 'Green', 'LightGreen', 'Lime', 'Yellow', 'Amber', 'Orange', 'DeepOrange', 'Brown', 'Gray', 'BlueGray']
        # key events support:
        Window.bind(on_key_down=self.on_key_down)
        Window.bind(on_key_up=self.on_key_up)
        
        return Builder.load_string(KV)
    
    ''' theme '''
    def change_theme(self):
        if self.theme_cls.theme_style == "Light":
            self.theme_cls.theme_style = "Dark"
            cfg.config_tree_['theme']['theme_style'] = "Dark"
        else:
            self.theme_cls.theme_style = "Light"
            cfg.config_tree_['theme']['theme_style'] = "Light"

    ''' theme-end '''

    ''' key events support'''
    def on_key_down(self, instance, keyboard, keycode, text, modifiers):
        # print(f"Key pressed: {text, modifiers}")
        if text == 'f' and modifiers == ['ctrl']:
            self.show_search_dialog()
        elif text == 'a' and modifiers == ['ctrl']:
            self.root.get_screen('main').children[0].children[0].children[-1].focus = True
        elif text == 'h' and modifiers == ['ctrl']:
            self.to_home()
        elif text == 's' and modifiers == ['ctrl']:
            self.to_settings()

    def on_key_up(self, instance, keyboard, keycode): ...
        # print(f"Key released: {keyboard, keycode}")
    ''' key events support-end '''

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
        self.root.get_screen('main').children[0].children[0].children[2].text = path
        self.root.get_screen('main').children[0].children[0].children[2].focus = True # = path
        toast(path)

    def exit_manager(self, *args):
        '''Called when the user reaches the root of the directory tree.'''

        self.manager_open = False
        self.file_manager.close()

    ''' file manager-end '''
    
    def check(self): # .children.__len__()
        # 
        text_field_text = self.root.get_screen('main').children[0].children[0].children[-1].text
        print('text_field_text:\n',self.root.get_screen('main').children[0].children[0].children[-1].text,text_field_text)
        text_field_text = self.root.get_screen('main').children[0].children[0].children[-1].text
        print('text_field_text:\n',self.root.get_screen('main').children[0].children[0].children[-1].text,text_field_text)
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
        self.root.get_screen('main').children[0].children[0].children[-1].text = 'name your memo'
        # self.root.get_screen('main').children[0].children[0].children[-1].text = 'name your memo'
        
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
                    on_text_validate = self.do_search
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
        def set_on_focus(root): # set focus to the text field
            root.focus = True 
        threading.Thread(target=Clock.schedule_once(lambda dt: set_on_focus(self.dialog.content_cls), 1 * 0.3)).start()

    def close_dialog(self,*args):
        self.dialog.dismiss()

    def do_search(self, obj):
        # serach-dialog-box content-API
        search_query = str(self.dialog.content_cls.text)
        #
        # Clock.schedule_once(lambda dt: self.show_modal('p'))
        print(f'Searching for: {search_query}')
        # search in db...
        t_ = db.query_db(search_query)
        # print(t_)
        # if already on results screen:
        # global results_widget_list
        if not self.root.current == 'results':
            # already cleared {skip deleting} ..
            # change screen to results
            self.root.current = 'results'
            # add result to results screen:
            # self.add_result([self.dialog.content_cls.text])
            Clock.schedule_once(lambda dt: self.add_result(t_) , 0.5)
            self.close_dialog()
        else:
            # clear the results screen first:
            self.delete_widget(None)
            # add result to results screen:
            # self.add_result([self.dialog.content_cls.text])
            Clock.schedule_once(lambda dt: self.add_result(t_) )
            self.close_dialog()
        #
        # threading.Thread(target=self.show_anim).start()

    ''' search end '''

    def my_exception_hook(self, *args):
        # close the db connection
        db.close_db_connection()
        print('db connection closed\nException:',args)
    def on_start(self):...
    def on_stop(self):
        # close the db connection
        db.close_db_connection()
        print('db connection closed')
        # save changes to config file:
        cfg.edit_config()
    
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
            print('content id :', content[0]) # id
            result_text = content[-1] # content
            result_url = content[-2] # url {file-dir}
            # print('result_text:', result_text, 'result_url:', result_url)
            item = OneLineListItem()
            box = item.children[0]
            box.orientation = 'horizontal'
            # box.spacing = 70
            # box = BoxLayout(orientation='horizontal', spacing=10)
            close_btn = MDIconButton(icon="close-circle", size_hint_x=None, width=50)
            close_btn.bind(on_release=lambda x: self.delete_from_db(id=content[0], widget_item=item))
            open_btn = MDIconButton(icon="open-in-new", size_hint_x=None, width=50)
            open_btn.bind(on_press=lambda x: toast('Opening {}'.format(result_url)))
            open_btn.bind(on_release=lambda x: self.open_dir(result_url))
            label = MDTextField(
                    text=result_text,
                    # size_hint_x=None,
                )
            box.add_widget(close_btn)
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
        if len(content) == 0:
            toast('No results found')
            self.root.get_screen('results').children[0].children[0].children[0].add_widget(
                _:=Image(source='./assets/404-error.png', size_hint=(None, None), size=(800, 800), pos_hint={'center_x': .5, 'center_y': .5})
            )
            results_widget_list.append(_)
        else:
            [add_content(i) for i in content ]  # 1 * i -> delay_sec
    
            print(len(results_widget_list))
            # threading.Thread(target=Clock.schedule_once(lambda dt: add_content(i), 1 * 0.1)).start()
            # threading.Thread(target=Clock.schedule_once(lambda dt: add_content(i), 1 * 0.1)).start()

    def delete_widget(self, r):
            global results_widget_list
            root = self.root.ids.container
            [root.remove_widget(w) for w in results_widget_list]
            # clear the list
            results_widget_list = []
    
    def delete_from_db( self, id:int, widget_item):
        # delete from db
        db.delete_data_by_id(id)
        # remove the widget from the results screen
        self.root.get_screen('results').children[0].children[0].children[0].remove_widget(widget_item)
        # toast:
        toast('Deleted successfully')
    
    ''' add result end '''

    ''' open file explorer '''
    def open_dir(self,dir_path:str):
        print('db used: ', db.db_path)
        ex.open_file_manager(dir_path)
        # try:
        #     print('opening dir:', dir_path) # for debugging
        #     subprocess.Popen('explorer "{}"'.format(dir_path), shell=True)
        # except Exception as e:
        #     toast('Error: {}'.format(e))
    ''' open file explorer end '''

    ''' home '''
    def to_home(self):
        self.root.current = 'main'
        # remove all widgets from results screen
        self.delete_widget(None)

    ''' home end '''

    ''' results-screen '''
    def to_settings(self):
        self.root.current = 'settings'

    ''' results-screen end '''

    ''' pdf-merger '''
    def to_merger(self):
        self.root.current = 'merger'
        # remove all widgets from results screen
        # self.delete_widget(None)

    ''' pdf-merger end '''

    ''' nerge-pdfs '''
    def merge_pdfs(self):
        # perform the merge operation
        # pick the input directory and save directory
        self.input_dir = mrg.select_directory("Select a folder that has all the pdf files")
        self.save_dir = mrg.select_directory(title_="Select a folder to save the merged pdf file")
        # start the spinner | self.active = True
        self.root.get_screen('merger').children[0].children[1].active = True
        # set the merged pdf name
        self.merged_pdf_name = str(os.path.basename(self.input_dir) + ' MERGED.pdf')

        def merge_in_background(root=None):

            # mrg.main() -> True {wait for true to call the callback}
            _ = mrg.merge_pdfs(input_dir=self.input_dir, dest_dir=self.save_dir, merged_pdf_name=self.merged_pdf_name)
            print(_)
            if _: root.active = False
            # set vars to '':
            self.input_dir = ''
            self.save_dir = ''
            self.merged_pdf_name = ''
        
        #
        threading.Thread(target=merge_in_background, args=((self.root.get_screen('merger').children[0].children[1]),)).start()
        # self.test('Merged PDF file saved to {}'.format(os.path.join(self.save_dir,self.merged_pdf_name).replace("/", "\\")))
        # Clock.schedule_once(lambda dt: merge_in_background(self.root.get_screen('merger').children[0].children[1]))
        # self.active = False
        # toast('Merged PDF file saved successfully')

    ''' backup '''
    def backup(self):
        # do backup:
        # 
        if not cfg.config_tree_['database']['backup_dir']:
            toast('Please select a backup directory')
            _ = sync.export_db(db.db_path)
            cfg.config_tree_['database']['backup_dir'] = _
            self.root.get_screen('settings').children[0].children[0].children[0].children[1].children[0].children[1].text = _

        else:
            sync.export_db(db.db_path, dst_path=cfg.config_tree_['database']['backup_dir'])
            toast('Backup successful {}'.format(get_date()))

    def select_backup_dir(self):
        # select backup dir
        _ = sync.select_directory()
        print('backup dir:', _)
        # save changes to config file:
        cfg.config_tree_['database']['backup_dir'] = _
        # # change the text of the text field
        self.root.get_screen('settings').children[0].children[0].children[0].children[1].children[0].children[1].text = _

    def test(self,content:str):
        # print(self.root.get_screen('settings').children[0].children[0].children[0].children[0].children[0].children[1].text)
        toast(content)
        # print('test'

    ''' backup end '''

    ''' restore '''
    def restore(self):
        # do import a backup:
        backup = sync.select_file(title_='Select a backup file to import')
        # sync.import_db(backup)
        print('backup:', backup)
        toast('Backup imported successfully')
        #
        # first make a copy of the selected db file to the current db path/dir
        sys_doc_dir = Path(os.path.expanduser("~/Documents"))
        import_file_dst_dir  = os.path.join(sys_doc_dir, 'TrackMyFiles')
            # copy file name:
        new_name_ = str('import_'+str(datetime.now().strftime("%Y-%m-%d %H-%M-%S")) + ".db")
        sync.copy_and_rename(src_path=backup, dst_dir=import_file_dst_dir, new_name=new_name_)
        # then change the db_path to the {selected db file-copy}:
        import_file_path = os.path.join(import_file_dst_dir, new_name_)
        # update changes{b/ackup path} to the config_file
        cfg.config_tree_['database']['path'] = import_file_path
        # change the text of the text field
        print('ZZxxx ',self.root.ids)
        self.root.ids.db_restore.text = backup
        # restart db:
        db.close_db_connection()
        db.db_path = import_file_path
        db.init()
        toast('Backup {} Restored successfully'.format(str(os.path.basename(backup))))
        
    ''' restore end '''
    ''' animation'''
    def show_anim(self):
        import  test_
        test_.show_modal(self, None)
    def show_modal(self, instance):
        modal = ModalView(size_hint=(.5, .5), auto_dismiss=True, background='', background_color=[0, 0, 0, 0])
        modal.add_widget(Image(source='./assets/gif.gif', anim_delay=0.03))  # Load and play the GIF
        modal.bind(on_open=self.modal_open, on_dismiss=self.modal_dismiss)
        modal.open()

    def modal_open(self, instance):
        instance.opacity = 0
        Animation(opacity=1, duration=0.5).start(instance)

    def modal_dismiss(self, instance):
        Animation(opacity=0, duration=0.5).start(instance)
        # instance.dismiss()

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

# global 

import merger as mrg
from kivy.animation import Animation
from kivy.uix.modalview import ModalView
from kivy.uix.image import Image

TrackMyFiles().run()