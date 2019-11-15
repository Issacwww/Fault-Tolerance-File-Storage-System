import subprocess
import shutil
import os
import sys
sys.path.append(sys.path[0] + "/..")
from util.constants import data_dir, b1_dir, b2_dir
from util.fileIO import build_dirs

build_dirs()
filename = 'backup1.py'

# provide the client data to the new node
def copy_files(source_dir, target_ir):
    for file in os.listdir(source_dir):
        source_file = os.path.join(source_dir, file)

        if os.path.isfile(source_file):
            shutil.copy(source_file, target_ir)


# protect the working node, if the working node failed, it would
# automatically recover the node 
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
