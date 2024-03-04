from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.navigationdrawer import MDNavigationDrawer

KV = '''
BoxLayout:
    orientation: 'vertical'

    MDTopAppBar:
        id: toolbar
        title: "Navigation Drawer"
        left_action_items: [['menu', lambda x: app.root.ids.nav_drawer.set_state("open") if app.root.ids.nav_drawer.state == "close" else app.root.ids.nav_drawer.set_state("close")]]

    ScreenManager:

    MDNavigationDrawer:
        id: nav_drawer

        BoxLayout:
            orientation: 'vertical'
            spacing: '8dp'
            padding: '8dp'

            Image:
                source: 'your_logo.png'

            MDFlatButton:
                text: 'Change Theme'
                on_release: app.change_theme()
'''

class MainApp(MDApp):
    def build(self):
        return Builder.load_string(KV)

    def change_theme(self):
        if self.theme_cls.theme_style == "Light":
            self.theme_cls.theme_style = "Dark"
        else:
            self.theme_cls.theme_style = "Light"

MainApp().run()