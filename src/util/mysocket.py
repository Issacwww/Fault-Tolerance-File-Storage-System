import pickle
from constants import DECODING, HEADER_SIZE, CHUNK_SIZE


def send_str_msg(s, msg):
    msg = pickle.dumps(msg)
    msg = bytes(f"{len(msg):<{HEADER_SIZE}}", DECODING) + msg
    s.send(msg)


def send_file(s, filepath):
    with open(filepath, 'rb', encoding=DECODING) as f:
        msg = pickle.dumps(f)
        msg = bytes(f"{len(msg):<{HEADER_SIZE}}", DECODING) + msg
        # print(msg)
        s.send(msg)


def recv_msg(s, file_flag):
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
                if file_flag:
                    print("File received, the content listed below:")
                else:
                    print("Full message received")
                break
    return pickle.loads(full_msg[HEADER_SIZE:])
