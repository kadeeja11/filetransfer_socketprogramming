# send

import socket
import os   #use the module os.path to deal with the path name
import hashlib
import struct

HOST = 'localhost'
PORT = 12345
BUFFER_SIZE = 1024
HEAD_STRUCT = '128sIq16s'


def cal_md5(file_path):
    with open(file_path, 'rb') as fr:
        md5 = hashlib.md5()
        md5.update(fr.read())
        md5 = md5.digest()
        return md5


def get_file_info(file_path):
    file_name = os.path.basename(file_path) #get the path basename as the file name
    file_name_len = len(file_name)  #get the length of file name
    file_size = os.path.getsize(file_path)  #Return the size, in bytes, of path.
    md5 = cal_md5(file_path)
    return file_name, file_name_len, file_size, md5


def send_file(file_path):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (HOST, PORT)

    file_name, file_name_len, file_size, md5 = get_file_info(file_path)

    #print(type(file_name), type(md5))
    file_head = struct.pack(HEAD_STRUCT, bytes(file_name, 'utf-8'), file_name_len, file_size, md5)
    print(md5)
    print("Start connect")
    sock.connect(server_address)
    sock.send(file_head)    #send the file head(file_info) first
    sent_size = 0   #set the sent_size as 0


    with open(file_path, 'rb') as fr:
        while sent_size < file_size:
            remained_size = file_size - sent_size
            send_size = BUFFER_SIZE if remained_size > BUFFER_SIZE else remained_size
            send_file = fr.read(send_size)
            sent_size += send_size
            sock.send(bytes(send_file))

if __name__ == '__main__':
    file_path = input('Please input file path:')    #input the file path
    if not file_path:
        file_path = 'test.txt'
    send_file(file_path)
