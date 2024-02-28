'''
OPEN FILE EXPLORER
'''

import os
import subprocess

def open_file_manager(dir_path):
    dir_path = dir_path.replace('/', '\\')
    if os.name == 'nt':  # For Windows
        os.startfile(dir_path)
    elif os.name == 'posix':  # For Linux, Mac
        subprocess.call(['open', dir_path])
# open_file_manager("C:\\Users\\Snehasish\\Downloads\\sample_mau5.jpg")
# open_file_manager("C:/Users/Snehasish/Downloads/telegram_bot")
# open_file_manager()
open_file_manager(r"C:\Users\Snehasish\Downloads\sample_mau5.jpg")


