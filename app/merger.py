'''
Merges PDF files from a specific directory & saves to a single pdf file in the choosen path directory.
'''


import os
import subprocess, time

# Check for all the dependencies are installed or not:
try:
    import datetime
    import tkinter as tk
    from tkinter import filedialog
    from PyPDF2 import PdfReader, PdfWriter
except ImportError:
    print('Dependencies are not installed. Install it using pip install PyPDF2')
    # Install dependencies using pip
    # subprocess.check_call(['pip', 'install', '-r', 'requirements.txt'])
    
global time_
time_ = str(datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S'))

# dir_picker function
def select_directory(title_:str="Select a folder that has all the pdf files") -> str:
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    dir_path = filedialog.askdirectory(title=title_)  # Open the directory dialog
    return dir_path

# merger function 
def merge_pdfs(dest_dir, input_dir, merged_pdf_name='merged.pdf') -> bool:  
    # from PyPDF2 import PdfReader, PdfWriter
    pdf_writer = PdfWriter()
    # input_dir = os.path.join(os.getcwd(), 'pdfs')
    # dest_dir = os.path.join(os.getcwd(), 'pdfs')
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.pdf'):
                file_path = os.path.join(root, file)
                pdf_reader = PdfReader(file_path)
                for page in pdf_reader.pages:
                    pdf_writer.add_page(page)
    
    # Save the merged PDF to a file
    # check if file doesnt exist, then create a new file:
    # time_ = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    # 
    # merged_pdf_name = 'merged.pdf'
    if not os.path.isdir(os.path.join(dest_dir,time_ ).replace('/', '\\')):
        # create a new directory with the current date and time:
        os.makedirs(os.path.join(dest_dir,time_).replace('/', '\\'))
        # create a new file {empty}:
        with open(os.path.join(dest_dir, time_,merged_pdf_name).replace('/', '\\'), 'wb') as fh:
            # try:
            #     fh.write()
            # except Exception as e: print(e)
            fh.close()
    with open(os.path.join(dest_dir, time_,merged_pdf_name).replace('/', '\\'), 'wb') as fh:
        pdf_writer.write(fh)
        fh.close()
    # 
    time.sleep(10)
    return True

# main function
# def main() -> True:
#     # select the directory that has all the pdf files:
#     input_dir = select_directory(title_="Select a folder that has all the pdf files")
#     # select the directory to save the merged pdf file:
#     dest_dir = select_directory(title_="Select a folder to save the merged pdf file")
#     # merge the pdf files:
#     merged_pdf_name = ''
#     # if (_:=input("Do you want to save the merged pdf file with a different name? (y/n) ").lower()) == 'y':
#     merged_pdf_name = str(os.path.basename(input_dir) + ' MERGED.pdf')
#     merge_pdfs(dest_dir, input_dir, merged_pdf_name=merged_pdf_name)
#     print('Merged PDF file saved to {}'.format(os.path.join(dest_dir, time_,merged_pdf_name).replace("/", "\\")))
#     # print(f'Merged PDF file saved to {os.path.join(dest_dir, "merged.pdf").replace("/", "\\")}')
#     # return True | for cALLBACKS
#     return True
# print(os.path.join(select_directory(title_="ABCD"),time_ ,'merged.pdf').replace('/', '\\'))




# from queue import Queue
# import threading
# import tkinter as tk
# from tkinter import filedialog
# from PyPDF2 import PdfWriter, PdfReader
# import os
# import datetime

# global time_
# time_ = str(datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S'))

# # Create a queue
# queue = Queue()

# # dir_picker function
# def select_directory(title_:str="Select a folder that has all the pdf files") -> str:
#     root = tk.Tk()
#     root.withdraw()  # Hide the root window
#     dir_path = filedialog.askdirectory(title=title_)  # Open the directory dialog
#     queue.put(dir_path)

# # merger function 
# def merge_pdfs(dest_dir, input_dir, merged_pdf_name='merged.pdf'):  
#     pdf_writer = PdfWriter()
#     for root, dirs, files in os.walk(input_dir):
#         for file in files:
#             if file.endswith('.pdf'):
#                 file_path = os.path.join(root, file)
#                 pdf_reader = PdfReader(file_path)
#                 for page in pdf_reader.pages:
#                     pdf_writer.add_page(page)
    
#     if not os.path.isdir(os.path.join(dest_dir,time_ ).replace('/', '\\')):
#         os.makedirs(os.path.join(dest_dir,time_).replace('/', '\\'))
#         with open(os.path.join(dest_dir, time_,merged_pdf_name).replace('/', '\\'), 'wb') as fh:
#             fh.close()
#     with open(os.path.join(dest_dir, time_,merged_pdf_name).replace('/', '\\'), 'wb') as fh:
#         pdf_writer.write(fh)
#         fh.close()

# # main function
# def main() -> True:
#     # select the directory that has all the pdf files:
#     input_dir = queue.get()
#     # select the directory to save the merged pdf file:
#     dest_dir = queue.get()
#     merged_pdf_name = str(os.path.basename(input_dir) + ' MERGED.pdf')
#     merge_pdfs(dest_dir, input_dir, merged_pdf_name=merged_pdf_name)
#     print('Merged PDF file saved to {}'.format(os.path.join(dest_dir, time_,merged_pdf_name).replace("/", "\\")))
#     # return True
#     queue.put(True)

# def merge_pdf_files():
#     # Start the thread {start the main thread first}
#     threading.Thread(target=main).start()

#     # # Get the directory paths in the main thread {use in gui}
#     select_directory("Select a folder that has all the pdf files")
#     select_directory("Select a folder to save the merged pdf file")
#     # # Wait for the main thread to finish
#     #
#     status = queue.get()
#     print('done from merger_func')
#     return status

# # while True:
# #     merge_pdf_files()
# #     _ = str(input('Press enter to merge pdf files '))
# #     if _ == 'exit':
# #         break
#     # else:

# print('done from merger.py')