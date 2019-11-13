import socket
import pickle
DECODING = 'utf-8'
HEADER_SIZE = 20
CHUNK_SIZE = 64

def send_str_msg():
    pass


def send_file(s, filepath):
    with open(filepath, 'rb', encoding=DECODING) as f:
        msg = pickle.dumps(f)
        msg = bytes(f"{len(msg):<{HEADER_SIZE}}", DECODING) + msg
        # print(msg)
        s.send(msg)


def recv_str_msg(s):
    full_msg = b''
    new_msg = True
    while new_msg:
        while True:
            msg = s.recv(CHUNK_SIZE)
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
    return full_msg


def recv_file():
    pass
