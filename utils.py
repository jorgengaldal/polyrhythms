import glob
import os

def clear_directory(path):
    dir = glob.glob(f"{path}/*")
    for file in dir:
        os.remove(file)