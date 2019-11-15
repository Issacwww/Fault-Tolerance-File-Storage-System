import subprocess
import shutil
import psutil
import os
import sys
sys.path.append(sys.path[0] + "/..")
from util.constants import data_dir, b1_dir, b2_dir
from util.fileIO import build_dirs

build_dirs()
filename = 'Snode.py'


def copy_files(source_dir, target_ir):
    for file in os.listdir(source_dir):
        source_file = os.path.join(source_dir, file)

        if os.path.isfile(source_file):
            shutil.copy(source_file, target_ir)


def save_pid():
    save_pids(data_dir)
    save_pids(b1_dir)
    save_pids(b2_dir)


def save_pids(data_path):
    pid = os.getpid()
    file = data_path + "pid1.txt"
    with open(file, 'w') as f:
        f.write(str(pid))


def get_pid():
    file = b1_dir + "pid1.txt"
    if os.path.exists(file):
        with open(file, 'r')as f:
            pid = f.read()
            return pid
    else:
        return '0'


def get_pid_child():
    file = b1_dir + "pid.txt"
    if os.path.exists(file):
        with open(file, 'r')as f:
            pid = f.read()
            return pid
    else:
        return '0'


def protection():
    while True:
        build_dirs()
        copy_files(b1_dir, data_dir)
        p = subprocess.Popen(['/bin/bash', '-i', '-c', 'python ' + filename], start_new_session=True).wait()

        """#if your there is an error from running python script, 
        the while loop will be repeated, 
        otherwise the program will break from the loop"""
        if p != 0:
            continue
        else:
            break


def protect():
    pid = int(get_pid_child())
    if pid:
        running_pids = psutil.pids()
        if pid in running_pids:
            pass
        else:
            save_pid()
            print("running backup1, pid: ", get_pid_child())
            protection()
    else:
        save_pid()
        print("running backup1, pid: ", get_pid_child())
        protection()


if __name__ == '__main__':
    while True:
        pid = int(get_pid())
        if pid:
            running_pids = psutil.pids()
            if pid in running_pids:
                pass
            else:
                save_pid()
                print("starting backup1, pid: ", get_pid())
                protect()
        else:
            save_pid()
            print("starting backup1, pid: ", get_pid())
            protect()
