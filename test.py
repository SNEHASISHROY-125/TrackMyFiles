
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.tooltip import MDTooltip

KV = '''
Screen:
    MDRaisedButton:
        text: "Hover me!"
        pos_hint: {"center_x": .5, "center_y": .5}
        tooltip_text: "This is a tooltip"
    MDTooltip:
        id: tooltip
        text: "This is a tooltip"
'''

class MainApp(MDApp):
    def build(self):
        return Builder.load_string(KV)

# MainApp().run()
    
# 
from pathlib import Path
import os

def get_documents_path():
    return Path(os.path.expanduser("~/Documents"))

print(get_documents_path())