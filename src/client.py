import socket
import sys
import os
import random
import pickle
from util.mysocket import *
from util.constants import CHUNK_SIZE, HEADER_SIZE,DECODING, REMOTE_ADDRESS, LOCAL_ADDRESS
# from util.metrics import Metrics
SERVER_IP = LOCAL_ADDRESS
# SERVER_IP = REMOTE_ADDRESS 

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

client_dir = f"./clients/{uid}"
create_random_files(client_dir, uid)

# generate request
request = " ".join(args[1:])
print(f"request: {request}")

# ask service provider
try:
    D_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("DEBUG: try to connect")
    D_socket.connect((SERVER_IP, 4000))

    # show connection success
    print("DEBUG: send request")
    msg, msg_bytes = recv_msg(D_socket,False)
    print(msg)

    # ask for service
    send_str_msg(D_socket, request)
    S_socket = None
    # receive response (and do '->' action if exist)
    # 1.connect                         D node return a ip address
    if order == "c":
        response_c,response_bytes = recv_msg(D_socket,False)
        print("your file would be stored with storage node, port:", response_c)

    # 2.add files                       D node return a ip address + add in D node-> connect with S node + add in S node
    elif order == "a":
        response_a,response_bytes = recv_msg(D_socket,False)
        print("now try to connect with storage node, port:", response_a)
        S_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        S_socket.connect((SERVER_IP, response_a)) 

        send_str_msg(S_socket, request)        
        # send the content of files using pickle
        for file in file_name:
            # TODO add metrics
            send_file(S_socket, client_dir, file)
            
            

    # 3.read file                       D node return a ip address-> connect with S node + read in S node
    elif order == "r":
        response_a,response_bytes = recv_msg(D_socket,False)

        print("now try to connect with storage node, port:", response_a)
        S_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        S_socket.connect((SERVER_IP, response_a))
        send_str_msg(S_socket, request)
        found, found_bytes = recv_msg(S_socket, False)
        if found:
            file_content, file_bytes = recv_msg(S_socket, True)
            print(f"Filename: {file_content[0]},\nContent:\n {file_content[1]}\nTotal Bytes:{file_bytes}")
        else:
            print("No such file")

    # 4.1.get file list (storage)       D node return a ip address-> connect with S node + S node return a list
    elif order == "s":
        response_gs,response_bytes = recv_msg(D_socket,False)
        print("now try to connect with storage node, port:", response_gs)
        S_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        S_socket.connect((SERVER_IP, response_gs))
        send_str_msg(S_socket, request)
        result_gs, result_bytes = recv_msg(S_socket,False)
        print("Files:", result_gs)


    # 4.2.get file list (directory)     D node return a list
    elif order == "d":
        # print("testing in gd!!!!")
        response_gd,response_bytes = recv_msg(D_socket,False)
        print("Files:", response_gd)
    # S_socket.close()
    # D_socket.close()
        

except Exception as e:
    print("sorry, bad connection, please try again.")
