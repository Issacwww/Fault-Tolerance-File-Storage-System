import socket
import sys
import os
import random

DECODING = "utf-8"


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
request = ""
for arg in args[1:]:
    request += arg + " "
print(f"request: {request}")

# ask service provider
try:
    D_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    D_socket.connect((socket.gethostname(), 4000))

    # show connection success
    msg = D_socket.recv(8192)
    print(msg.decode(DECODING))

    # ask for service
    D_socket.send(bytes(request, DECODING))

    # receive response (and do '->' action if exist)
    # 1.connect                         D node return a ip address
    if order == "c":
        response_c = int(D_socket.recv(8192).decode(DECODING))
        print("your file would be stored with storage node, port:", response_c)

    # 2.add files                       D node return a ip address + add in D node-> connect with S node + add in S node
    elif order == "a":
        response_a = int(D_socket.recv(8192).decode(DECODING))
        print("now try to connect with storage node, port:", response_a)
        S_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        S_socket.connect((socket.gethostname(), response_a))
        S_socket.send(bytes(request, DECODING))
        # TODO completing the adding in S node
        #  (directory already added, you need to finish the upload part)

    # 3.read file                       D node return a ip address-> connect with S node + read in S node
    elif order == "r":
        response_a = int(D_socket.recv(8192).decode(DECODING))
        print("now try to connect with storage node, port:", response_a)
        S_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        S_socket.connect((socket.gethostname(), response_a))
        S_socket.send(bytes(request, DECODING))
        # TODO after finish the upload, now you can read the file in Sndoe and send the str back,
        #  you need to
        #  1.in Snode.py get the file context
        #  2.recv the str send by Snode
        #  3.print it here

    # 4.1.get file list (storage)       D node return a ip address-> connect with S node + S node return a list
    elif order == "s":
        response_gs = int(D_socket.recv(8192).decode(DECODING))
        print("now try to connect with storage node, port:", response_gs)
        S_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        S_socket.connect((socket.gethostname(), response_gs))
        S_socket.send(bytes(request, DECODING))
        result_gs = S_socket.recv(8192)
        print("files:", result_gs.decode(DECODING))

    # 4.2.get file list (directory)     D node return a list
    elif order == "d":
        print("testing in gd!!!!")
        response_gd = D_socket.recv(8192)
        print("files:", response_gd.decode(DECODING))

except Exception as e:
    # print(e)
    print("sorry, bad connection, please try again.")
