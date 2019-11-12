import subprocess
import shutil
import os

data_dir = "./data/"
b1_dir = "./data1/"
b2_dir = "./data2/"


def build_dirs():
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    if not os.path.exists(b1_dir):
        os.makedirs(b1_dir)
    if not os.path.exists(b2_dir):
        os.makedirs(b2_dir)


build_dirs()
filename = 'backup1.py'


def copy_files(source_dir, target_ir):
    for file in os.listdir(source_dir):
        source_file = os.path.join(source_dir, file)

        if os.path.isfile(source_file):
            shutil.copy(source_file, target_ir)


def protect():
    while True:
        build_dirs()
        copy_files(b2_dir, b1_dir)
        p = subprocess.Popen(['/bin/bash', '-i', '-c', 'python ' + filename], start_new_session=True).wait()

        """#if your there is an error from running python script, 
        the while loop will be repeated, 
        otherwise the program will break from the loop"""
        if p != 0:
            continue
        else:
            break


protect()
