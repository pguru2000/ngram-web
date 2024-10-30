import nltk
from tqdm import tqdm
import numpy as np
import argparse
from .configure import *
import os
import pathlib
import _thread

import string
import matplotlib.pyplot as plt
import pandas as pd
from pandas.plotting import table
import pytz
from datetime import datetime

global check_process
check_process = []
for i in range(count_process):
    check_process.append([0, 0])

def generate_result_txt(file_count):
    
    hist = np.zeros((101, file_count), np.uint8)
    for file_title in os.listdir(result_path):
        if file_title.endswith('.npy'):
            file_path = os.path.join(result_path, file_title)
            his = np.load(file_path)
            hist |= his
    #         os.remove(file_path)

    # os.remove(gram_file)
    hist_sum = np.sum(hist, axis=1, dtype=np.uint32)
    with open('result/result.txt', 'w') as the_file:
        for i, h in enumerate(hist_sum):
            result = str(i + 1) + ' | ' + str(h) + '\n'
            the_file.write(result)

def get_result(index, file_count):
    print("Processing: ", index)   

    total_n_grams = list(np.load(gram_file, allow_pickle=True))
    step = int(file_count / count_process)

    pro_arr = []

    for i in range(file_count):
        if index == i % count_process:
            pro_arr.append(i)

    total_num = len(pro_arr)

    global check_process
    check_process[index] = [0, total_num]
    pbar = tqdm(total=total_num)
    result = np.zeros((101, file_count), np.uint8)
    spec_files = ''
    #for i in range(start_idx, end_idx):
    # print(pro_arr)

    for processed_num, i in enumerate(pro_arr):
        f1_gram = total_n_grams[i]

        his = []
        for j in range(i + 1, file_count):
            f2_gram = total_n_grams[j]
            distance = nltk.jaccard_distance(set(f1_gram), set(f2_gram))
            distance = 100 - int(distance * 100)
            # result[distance][i] = 1
            # result[distance][j] = 1
            for k in range(distance, 101):
                result[k][i] = 1
                result[k][j] = 1
        pbar.update(1)
        check_process[index] = [processed_num+1, total_num]

    pbar.close()

    file_path = 'result/{:02d}.npy'.format(index)
    np.save(file_path, result)
    return True

def filecount():
    file_count = 0
    for path in pathlib.Path('uploads/origfiles').iterdir():
        if path.is_file():
            file_count += 1
    return file_count

def file_save_action():
    tz_paris = pytz.timezone('Europe/Paris')
    now = datetime.now(tz_paris)
    result_file_name = "analyse-de-similarite-" + '{:02d}'.format(now.day) + "-" + '{:02d}'.format(now.month)

    ax = plt.subplot(111, frame_on=False)
    ax.figure.set_size_inches(5, 20)
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)

    rows, cols = 5, 10
    labels = ['Taux de similitude','Nombre de textes']

    result_arr = []
    result_txt = 'result/result.txt'
   
    with open(result_txt, 'r') as rows:
        for i, row in enumerate(rows):
            result_arr.append([row.split(' | ')[0], row.split(' | ')[1].strip('\n')])

    # df = pd.DataFrame(np.random.randint(0, 100, size=(100, 2)), columns=labels)
    df = pd.DataFrame(result_arr, columns=labels)
    
    table(ax, df, loc='center')  # where df is your data frame
    
    plt.savefig('static/result/' + result_file_name + '.png')
    plt.savefig('static/result/' + result_file_name + '.pdf')
    return result_file_name

def startprocess():
    global check_process
    check_process = []

    file_count = filecount()
    print('file_count:', file_count )
    _finished_list = []
    for i in range(count_process):
        _finished_list.append(False)
        check_process.append([0, 0])
    try:    
        for i in range(count_process):
            _finished_list[i] = _thread.start_new_thread( get_result, (i, file_count) )        
            print("thread----", i ,  " started")
            
    except:
        print(" Error: unable to start thread ")

    while 1:
        _finished = True
        for i in range(count_process):
            if _finished_list[i] == False:
                _finished = False
                break
        if _finished == False:
            pass
        else:
            generate_result_txt(file_count)
            result_file_name = file_save_action()
            return result_file_name

def checkprocess():
    global check_process
    
    print('check process')
    print(check_process)
    return check_process