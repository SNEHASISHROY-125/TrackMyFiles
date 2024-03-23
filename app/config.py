'''
App Configuaration
'''

import os
import json
from pathlib import Path

global config_path

# check if config file exists
def check_config():
    global config_path
    dir_path = os.path.dirname(os.path.abspath(__file__))
    sys_doc_dir = Path(os.path.expanduser("~/Documents"))
    config_path = os.path.join(sys_doc_dir, 'TrackMyFiles','config.json')
    if not os.path.exists(config_path):
        # create app directory:
        os.makedirs(os.path.join(sys_doc_dir, 'TrackMyFiles'), exist_ok=True)
        with open(config_path, 'w') as f:
            print('config file created')
            config_tree_ = {
                'database': {
                    'path': os.path.join(sys_doc_dir, 'TrackMyFiles', 'my_database.db'),
                    'backup_dir': '',
                    'auto_backup': False
                },
                'sign_in_status': {
                    'status': False,
                },
                'theme': {
                    'primary_palette': 'Teal',
                    'accent_color': 'Red',
                    'theme_style': 'Light'
                },
                'app': {
                    'version': '1.0.0',
                    'first_run': True,
                    'last_opened': '',
                    'last_backup': '',
                    'memo_text_limit': 15,
                }
            }
            json.dump(config_tree_, f)
            f.close()

# load config file
def load_config() -> dict:
    global config_path
    with open(config_path, 'r') as f:
        config = json.load(f)
        f.close()
        return config

# print(load_config())

def edit_config() -> None:
    global config_path
    with open(config_path, 'w') as f:
        json.dump(config_tree_, f)
        f.close()
    # json.dump(tree_, open(r'.\\app\\config.json', 'w'))

# config_tree_['sign_in_status']['status'] = True
# edit_config()

# check:
check_config()

# load:
global config_tree_
config_tree_ = load_config()
