
'''
TESTING | UI

-- List view to dissplay search results
'''


from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.list import OneLineAvatarIconListItem
from kivymd.uix.button import MDIconButton
import time , threading

KV = '''
ScrollView:
    MDList:
        id: container
'''

from kivy.clock import Clock
from kivymd.uix.textfield import MDTextField

from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.list import OneLineListItem
from kivymd.uix.button import MDIconButton
from kivymd.uix.label import MDLabel

class Example(MDApp):
        def build(self):
            return Builder.load_string(KV)

        def on_start(self):
            result_text = ''
            item = OneLineListItem()
            box = BoxLayout(orientation='horizontal', spacing=10)
            icon_btn1 = MDIconButton(icon="android", size_hint_x=None, width=50)
            icon_btn2 = MDIconButton(icon="apple", size_hint_x=None, width=50)
            label = MDTextField(
                    text=result_text,
                )
            box.add_widget(icon_btn1)
            box.add_widget(label)
            box.add_widget(icon_btn2)
            item.add_widget(box)
            # root.add_widget(item)
            self.root.ids.container.add_widget(item)
            # time.sleep(2)
            # threading.Thread(target=self.add_widget_with_time,args=(self.root.ids.container,)).start()

        def add_widget_with_time(self, root):
            """
            Adds widgets to the root with a time delay.

            Args:
                root: The root widget to which the widgets will be added.

            Returns:
                None
            """
            for i in range(5):  # 1 * i -> delay_sec
                Clock.schedule_once(lambda dt: self.add_widget(root, i), 1 * i)

        def add_widget(self, root, i):
            global widget_list
            item = OneLineAvatarIconListItem()
            text_field = MDTextField(hint_text=f'Item {i}')
            icon_btn = MDIconButton(icon="android")
            item.children[0].add_widget(text_field)
            item.children[0].add_widget(icon_btn)
            icon_btn = MDIconButton(icon="android")
            item.children[0].add_widget(icon_btn)
            root.add_widget(item)
            # store the widgets to remove in future
            widget_list.append(item)
        
        def delete_widget(self, r):
            global widget_list
            root = self.root.ids.container
            [root.remove_widget(w) for w in widget_list]

    # Example().run()
    # 

# add or delete widgets from main widget tree
global widget_list
widget_list = []


Example().run()