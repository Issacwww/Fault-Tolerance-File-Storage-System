import socket
import sys
import os
import random
import pickle

DECODING = "utf-8"

CHUNK_SIZE = 1024
HEADER_SIZE = 10


# generate random file for client
def create_random_files(dir, id):
    if not os.path.exists(dir):
        os.makedirs(dir)
        for i in range(random.randint(10, 20)):
            with open(dir + "/" + str(i), 'w') as f:
                s = ""
                for j in range(random.randint(0, 100)):
                    s += str(id) + " generated random sentence " + str(j + 1) + "\n"
                f.write(s)


# read args
args = sys.argv
uid = args[1]
order = args[2]
if len(args) > 3:
    file_name = args[3:]
    print("filename: ", file_name)

client_dir = "./clients/" + uid
create_random_files(client_dir, uid)

# generate request
request = "".join(args[1:])
print(f"request: {request}")

# ask service provider
try:
    D_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    D_socket.connect((socket.gethostname(), 4000))

    # show connection success
    msg = D_socket.recv(CHUNK_SIZE)
    print(msg.decode(DECODING))

    # ask for service
    D_socket.send(bytes(request, DECODING))
    S_socket = None
    # receive response (and do '->' action if exist)
    # 1.connect                         D node return a ip address
    if order == "c":
        response_c = int(D_socket.recv(CHUNK_SIZE).decode(DECODING))
        print("your file would be stored with storage node, port:", response_c)

    # 2.add files                       D node return a ip address + add in D node-> connect with S node + add in S node
    elif order == "a":
        response_a = int(D_socket.recv(CHUNK_SIZE).decode(DECODING))
        print("now try to connect with storage node, port:", response_a)
        S_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        S_socket.connect((socket.gethostname(), response_a))
        S_socket.send(bytes(request, DECODING))
        # send the content of files using pickle
        for file in file_name:
            with open(client_dir + '/' + file, 'rb', encoding=DECODING) as f:
                msg = pickle.dumps(f.readlines())
                msg = bytes(f"{len(msg):<{HEADER_SIZE}}", DECODING) + msg
                print(msg)
                S_socket.send(msg)

    # 3.read file                       D node return a ip address-> connect with S node + read in S node
    elif order == "r":
        response_a = int(D_socket.recv(CHUNK_SIZE).decode(DECODING))
        print("now try to connect with storage node, port:", response_a)
        S_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        S_socket.connect((socket.gethostname(), response_a))
        S_socket.send(bytes(request, DECODING))
        # TODO after finish the upload, now you can read the file in Sndoe and send the str back,
        #  you need to
        #  1.in Snode.py get the file context
        #  2.recv the str send by Snode
        #  3.print it here
        full_msg = b''
        new_msg = True
        while new_msg:
            while True:
                msg = S_socket.recv(CHUNK_SIZE)
                if new_msg:
                    print("new msg len:", msg[:HEADER_SIZE])
                    msglen = int(msg[:HEADER_SIZE])
                    new_msg = False
                print(f"full message length: {msglen}")
                full_msg += msg
                print(len(full_msg))
                if len(full_msg) - HEADER_SIZE == msglen:
                    print("File received, the content listed below:")
                    print(pickle.loads(full_msg[HEADER_SIZE:]))
                    break

    # 4.1.get file list (storage)       D node return a ip address-> connect with S node + S node return a list
    elif order == "s":
        response_gs = int(D_socket.recv(CHUNK_SIZE).decode(DECODING))
        print("now try to connect with storage node, port:", response_gs)
        S_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        S_socket.connect((socket.gethostname(), response_gs))
        S_socket.send(bytes(request, DECODING))
        result_gs = S_socket.recv(CHUNK_SIZE)
        print("files:", result_gs.decode(DECODING))

    # 4.2.get file list (directory)     D node return a list
    elif order == "d":
        print("testing in gd!!!!")
        response_gd = D_socket.recv(CHUNK_SIZE)
        print("files:", response_gd.decode(DECODING))
        
    S_socket.close()
    D_socket.close()


except Exception as e:
    # print(e)
    print("sorry, bad connection, please try again.")
