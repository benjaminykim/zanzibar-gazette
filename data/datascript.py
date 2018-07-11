import os
import subprocess
from os.path import isfile, join

def explore(filepath):
    files = []
    for item in os.listdir(filepath):
        if item.endswith(".pdf"):
            files.append(join(filepath, item))
            continue
        if not isfile(item):
            files += explore(join(filepath, item))
    return files



def convert_to_pdf(files):
    for item in files:
        item_txt = item.split(".")[0] + ".txt"
        subprocess.call(["python3", os.getcwd() + "/pdf2txt.py", item, "-o", item_txt])

convert_to_pdf(explore(os.getcwd()))

