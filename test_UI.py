
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

class Example(MDApp):
        def build(self):
            return Builder.load_string(KV)

        def on_start(self):
            item = OneLineAvatarIconListItem(text=f'Item first, 8')
            icon_btn = MDIconButton(icon="android")
            item.children[0].add_widget(icon_btn)
            self.root.ids.container.add_widget(item)
            # time.sleep(2)
            threading.Thread(target=self.add_widget_with_time,args=(self.root.ids.container,)).start()

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
            item = OneLineAvatarIconListItem(text=f'Item {i}')
            icon_btn = MDIconButton(icon="android")
            item.children[0].add_widget(icon_btn)
            root.add_widget(item)

    # Example().run()
    # 

Example().run()