import os
from shutil import copyfile
import zipfile

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import configure

input_txt_dir = configure.input_txt_dir
result_path = configure.result_path

try:
    os.mkdir(input_txt_dir)
except:
    for file_title in os.listdir(input_txt_dir):
        if file_title.endswith(".txt"):
            file_path = os.path.join(input_txt_dir, file_title)
            os.remove(file_path)
try:
    os.mkdir(result_path)
except:
    for file_title in os.listdir(result_path):
        #if file_title.endswith(".txt"):
        file_path = os.path.join(result_path, file_title)
        os.remove(file_path)


def UploadAction(event=None):
    input_filepath = filedialog.askopenfilename(filetypes=[("Zip files", "*.zip")])    
    if input_filepath != '':
        input_filename = os.path.split(input_filepath)[1]        
        input_filename = input_filename.replace('[]', '')
        
        # dest_filepath = f'{os.getcwd()}/{input_txt_dir}/{input_filename}'
        dest_filepath = os.path.join(f'{input_txt_dir}', f'{input_filename}')
        copyfile(input_filepath, dest_filepath)

        unzip(dest_filepath)

def unzip(dest_filepath):  
    zip_file = zipfile.ZipFile(dest_filepath, 'r')
    with zip_file:
        try:
            zip_file.extractall(os.path.split(dest_filepath)[0])
            
            messagebox.showinfo(title=None, message="Zip file upload success")
        except:
            messagebox.showinfo(title=None, message="Zip file Error.")
    
    # btn_file_open.pack_forget()
    # btn_ngram_cal.pack()
    os.remove(dest_filepath)
    root.destroy()

def NgramCal():
    calc_ngram.make_gram_file()

root = tk.Tk(className='Upload batch of text files')
root.geometry("500x200")
btn_file_open = tk.Button(root, text='Open Zip file', command=UploadAction)
btn_file_open.pack()

btn_ngram_cal = tk.Button(root, text='N-gram calculate', command=NgramCal)

root.mainloop()