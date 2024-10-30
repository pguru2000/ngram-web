import string
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pandas.plotting import table

import os
import pytz
from datetime import datetime

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
    
    plt.savefig('result/' + result_file_name + '.png')
    plt.savefig('result/' + result_file_name + '.pdf')