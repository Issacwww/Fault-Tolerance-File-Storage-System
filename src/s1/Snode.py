import socket
import threading
import shutil
import psutil
import json
import os
import time
import sys
sys.path.append(sys.path[0] + "/..")
from util.mysocket import *
from util.constants import *
from util.fileIO import build_dirs
from util.metrics import Metrics

build_dirs()
# save files to 3 dir 
def store_file(uid, file):
    store_file_copy(data_dir+'/'+uid,file)
    store_file_copy(b1_dir+'/'+uid,file)
    store_file_copy(b2_dir+'/'+uid,file)

# store uploaded file
def store_file_copy(dir, file):
    if not os.path.exists(dir):
        os.makedirs(dir)
    with open(dir+'/'+file[0],'w') as w:
        w.write(file[1])

# always backup client data to all nodes
def save_clients_data(client_file):
    # store all data into data folder and backup folder
    save_clients_copy(data_dir, client_file)
    save_clients_copy(b1_dir, client_file)
    save_clients_copy(b2_dir, client_file)


def save_clients_copy(dir, client_file):
    with open(dir + CLIENT_FILE, 'w') as f:
        json.dump(client_file, f, sort_keys=True, indent=4, separators=(',', ': '))
        
# receive file from client
def provide_service(connection, client_file, metrics):
    command, command_bytes = recv_msg(connection, False)
    command = command.split()
    uid = command[0]
    order = command[1]
    if len(command) > 2:
        file_name = command[2:]
    print(f"msg from client {uid} with command {command}")
    # update metrics
    metrics.addOne(REQUEST_NUM)
    metrics.addValue(DATA_TRANSFER,command_bytes)
    start = time.time()
    if order == "a":
        if uid not in client_file:
            client_file[uid] = list()
        temp_file_list = client_file[uid]
        for file in file_name:
            if file not in temp_file_list:
                print(f"file {file} will be added to Snode")
                temp_file_list.append(file)
            else:
                print(f"file {file} already exist, update it")

            # TODO download file to data folder and backup folder
            f, f_bytes = recv_msg(connection, True)
            store_file(uid,f)

            metrics.addValue(DATA_TRANSFER,f_bytes)
            print(f"file {file} uploaded to Snode")

        client_file[uid] = temp_file_list

    elif order == "r":
        temp_file_list = client_file[uid]
        msg_bytes = 0
        if len(file_name) > 1:
            print("Only allowed to read one file at a time, return the first required file")
        if file_name[0] not in temp_file_list:
            msg_bytes += send_str_msg(connection, False)
        else:
            msg_bytes += send_str_msg(connection, True)
            msg_bytes += send_file(connection, data_dir+"/"+uid,file_name[0])
        metrics.addValue(DATA_TRANSFER,msg_bytes)
        
    elif order == "s":
        if uid not in client_file:
            client_file[uid] = list()
        result = " ".join(client_file[uid])
        msg_bytes = send_str_msg(connection, result)
        metrics.addValue(DATA_TRANSFER,msg_bytes)

    end = time.time()
    metrics.addValue(LATENCY, end - start)
    metrics.emit()
    # store all data into data folder and backup folder
    save_clients_data(client_file)


def init_dicts(dict_name):
    if os.path.exists(data_dir + dict_name):
        with open(data_dir + dict_name) as f:
            return json.load(f)
    else:
        return dict()

# provide service
def testing(metrics):
    client_file = init_dicts(CLIENT_FILE)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # ipv4, tcp
    s.bind((socket.gethostname(), 5000))  # host, port
    s.listen(5000)
    # accept multi requests
    while True:
        # connect with client
        client_connection, address = s.accept()
        service = threading.Thread(target=provide_service, args=(client_connection, client_file,metrics))
        service.setDaemon(True)
        service.start()


#  copy all data from backup into new location for the new working node, 
#  so the working node would have the pid info and all client data it needs to recover from the failure.
def copy_files(source_dir, target_ir):
    for file in os.listdir(source_dir):
        source_file = os.path.join(source_dir, file)

        if os.path.isfile(source_file):
            shutil.copy(source_file, target_ir)

# save pid to all nodes, in case one/two node(s) failed
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
    file = data_dir + "pid.txt"
    if os.path.exists(file):
        with open(file, 'r')as f:
            pid = f.read()
            return pid
    else:
        return '0'


if __name__ == '__main__':
    while True:
        pid = int(get_pid())
        
        # check if this program already running
        if pid:
            running_pids = psutil.pids()
            if pid in running_pids:
                pass
            else:
                save_pid()
                print("starting Dnode, pid: ", os.getpid())
                # build metric
                metrics = Metrics(os.getpid())
                # start server
                testing(metrics)
        else:
            save_pid()
            print("starting Dnode, pid: ", os.getpid())
            # build metric
            metrics = Metrics(os.getpid())
            # start server
            testing(metrics)

    # pid = os.getpid()
    # print("starting Dnode, pid: ",pid)
    # metrics = Metrics(pid)
    # testing(metrics)