import zipfile
import json
from datetime import datetime

from os import listdir
from os.path import isfile, join
import re
import os
import random
from random import randint
import string
import sys


def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def unzip(path, destfolder):
    zip = zipfile.ZipFile(path)
    zip.extractall(destfolder)
    zip.close()
    pass

def delete_files(path):
    for f in listdir(path):
        file_path = os.path.join(path, f)
        if os.path.isfile(file_path):
            os.remove(file_path)

def zip(path, destname):
    ziper = zipfile.ZipFile(destname, mode = 'w', compression=zipfile.ZIP_DEFLATED)
    origfiles = [f for f in listdir(path) if isfile(join(path, f))]
    for i in range(len(origfiles)):
        #ziper.write(join(path, origfiles[i]), "result/" + origfiles[i], zipfile.ZIP_DEFLATED)
        ziper.write(join(path, origfiles[i]), origfiles[i], zipfile.ZIP_DEFLATED)
    ziper.close()
    pass

def iszipfile(file_name):
    return zipfile.is_zipfile(file_name)