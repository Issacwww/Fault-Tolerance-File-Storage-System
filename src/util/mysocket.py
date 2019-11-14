import pickle
from .constants import DECODING, HEADER_SIZE, CHUNK_SIZE


def send_str_msg(s, msg):
    msg = pickle.dumps(msg)
    msg = bytes(f"{len(msg):<{HEADER_SIZE}}", DECODING) + msg
    s.send(msg)
    # return len(msg)

def send_file(s, dir, filename):
    path = f"{dir}/{filename}"
    with open(path, 'r') as f:
        msg = pickle.dumps((filename,f.read()))
        msg = bytes(f"{len(msg):<{HEADER_SIZE}}", DECODING) + msg
        s.send(msg)
    
    # return len(msg)

def recv_msg(s,file_flag):
    full_msg = []
    msglen,recvlen = 0, 0
    new_msg = True
    while new_msg:
        if msglen == 0:
            header = s.recv(HEADER_SIZE)
            msglen = int(header)
            new_msg = False
            print(f"full message length: {msglen}")
        while recvlen < msglen:
            chuck = s.recv(min(msglen - recvlen, CHUNK_SIZE))
            if chuck == b'':
                raise RuntimeError("socket connection broken")
            full_msg.append(chuck)
            recvlen += len(chuck)
        
        if file_flag:
            print("File received!")
        else:
            print("Full message received!")
    return pickle.loads(b''.join(full_msg)), msglen+HEADER_SIZE
    # while new_msg:
    #     while True:
    #         msg = s.recv(CHUNK_SIZE)
    #         if new_msg:
    #             msglen = int(msg[:HEADER_SIZE])
    #             new_msg = False
    #             print(f"full message length: {msglen}")
    #         full_msg += msg
    #         if len(full_msg) - HEADER_SIZE >= msglen:
    #             if file_flag:
    #                 print("File received!")
    #             else:
    #                 print("Full message received")
    #             break
    # return pickle.loads(full_msg[HEADER_SIZE:]), len(full_msg)