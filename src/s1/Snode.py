import socket
import threading
import shutil
import psutil
import json
import os

DECODING = "utf-8"
data_dir = "./data/"
b1_dir = "./data1/"
b2_dir = "./data2/"
CLIENT_FILE = "client_file.txt"
if not os.path.exists(data_dir):
    os.makedirs(data_dir)
if not os.path.exists(b1_dir):
    os.makedirs(b1_dir)
if not os.path.exists(b2_dir):
    os.makedirs(b2_dir)


def save_clients_data(client_file):
    # store all data into data folder and backup folder
    save_clients_copy(data_dir, client_file)
    save_clients_copy(b1_dir, client_file)
    save_clients_copy(b2_dir, client_file)


def save_clients_copy(dir, client_file):
    with open(dir + CLIENT_FILE, 'w') as f:
        f.write(json.dumps(client_file, sort_keys=True, indent=4, separators=(',', ': ')))
    # TODO save files to 3 dir too


def provide_service(connection, client_file):
    command = connection.recv(8192).decode(DECODING).split()
    uid = command[0]
    order = command[1]
    if len(command) > 2:
        file_name = command[2:]

    if order == "a":
        if uid not in client_file:
            client_file[uid] = list()
        temp_file_list = client_file[uid]
        for file in file_name:
            if file not in temp_file_list:
                print(f"file {file} is added to Snode")
                temp_file_list.append(file)
            else:
                print(f"file {file} already exist")

            # TODO download file to data folder and backup folder
        client_file[uid] = temp_file_list

    elif order == "r":
        # TODO send back the file context
        print("TODO")

    elif order == "s":
        if uid not in client_file:
            client_file[uid] = list()
        result = ""
        for file in client_file[uid]:
            result += file + " "
        print(result)
        connection.send(bytes(result, DECODING))


    # store all data into data folder and backup folder
    save_clients_data(client_file)


def init_dicts(dict_name):
    if os.path.exists(data_dir + dict_name):
        with open(data_dir + dict_name) as f:
            return json.load(f)
    else:
        return dict()


def testing():
    client_file = init_dicts(CLIENT_FILE)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # ipv4, tcp
    s.bind((socket.gethostname(), 5000))  # host, port
    s.listen(5000)
    # accept multi requests
    while True:
        # connect with client
        client_connection, address = s.accept()
        service = threading.Thread(target=provide_service, args=(client_connection, client_file))
        service.setDaemon(True)
        service.start()


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
        if pid:
            running_pids = psutil.pids()
            if pid in running_pids:
                pass
            else:
                save_pid()
                print("starting Dnode, pid: ", get_pid())
                testing()
        else:
            save_pid()
            print("starting Dnode, pid: ", get_pid())
            testing()
