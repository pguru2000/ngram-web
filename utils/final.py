import nltk
from tqdm import tqdm
import numpy as np
import argparse
from configure import *
import os
from shutil import copyfile
from tqdm import tqdm
import zipfile
import pathlib

# Get the number of files in input folder
file_count = 0
for path in pathlib.Path(input_txt_dir).iterdir():
    if path.is_file():
        file_count += 1
print(file_count)


try:    
    os.mkdir(threhold_file_dir)    
except:
    for file_title in os.listdir(threhold_file_dir):
        #if file_title.endswith(".txt"):
        file_path = os.path.join(threhold_file_dir, file_title)        
        os.remove(file_path)

parser = argparse.ArgumentParser()
parser.add_argument("--idx", type=int, help="the index of the script")
parser.add_argument("--count", type=int, help="the cont of the scripts")
args = parser.parse_args()

# file_dir = f'../{file_dir}'
file_dir = input_txt_dir

if args.idx == 100:
    hist = np.zeros((101, file_count), np.uint8)
    for file_title in os.listdir(result_path):
        if file_title.endswith('.npy'):
            file_path = os.path.join(result_path, file_title)
            his = np.load(file_path)
            hist |= his
            os.remove(file_path)

    os.remove(gram_file)
    hist_sum = np.sum(hist, axis=1, dtype=np.uint32)

    result_txt = '../result.txt'
    with open(result_txt, 'w') as the_file:
        for i, h in enumerate(hist_sum):
            result = str(i) + ' | ' + str(h) + '\n'
            the_file.write(result)


    ##### Make zip file with threhold value #####
    sel_no_list = []
    for i, h in enumerate(hist[select_no]):
        if h == 1:
            sel_no_list.append(i)
    
    i = -1
    for file_title in os.listdir(file_dir):
        if file_title.endswith(".txt"):
            src_file_path = os.path.join(file_dir, file_title)
            dest_file_path = os.path.join(threhold_file_dir, file_title)
            i = i+1
            if i in sel_no_list:
                copyfile(src_file_path, dest_file_path)
            os.remove(src_file_path)

    # writing files to a zipfile & deleting files in threhold folder
    zip_file = zipfile.ZipFile('../threhold_files.zip', 'w')
    with zip_file:
        print('zipping files...')       
        for file_title in tqdm(os.listdir(threhold_file_dir)):
            file_path = os.path.join(threhold_file_dir, file_title)            
            zip_file.write(file_path)
            os.remove(file_path)