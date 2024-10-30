from nltk import ngrams
import os
from .configure import *
import numpy as np
from tqdm import tqdm
import pathlib

global check_process
check_process = 0

def get_ngrams(text, n):
    n_grams = ngrams(text, n)
    return [' '.join(grams) for grams in n_grams]

def create_gram_file():
    try:
        total_n_grams = []
        
        file_dir = 'uploads/origfiles'
        global check_process
        no = 0
        for file_title in tqdm(os.listdir(file_dir)):
            if file_title.endswith(".txt"):
                file_path = os.path.join(file_dir, file_title)
                f = open(file_path, "r", encoding="utf8")
                text = f.read()
                for re_str in re_strs:
                    text = text.replace(re_str, ' ')
                total_n_grams.append(get_ngrams(text.split(), n))
                f.close()
                no = no + 1
                check_process = no

        np.save(gram_file, total_n_grams)
        return True
    except:
        return False

def filecount():
    file_count = 0
    for path in pathlib.Path('uploads/origfiles').iterdir():
        if path.is_file():
            file_count += 1
    return file_count

def checkprocess():
    global check_process
    return check_process