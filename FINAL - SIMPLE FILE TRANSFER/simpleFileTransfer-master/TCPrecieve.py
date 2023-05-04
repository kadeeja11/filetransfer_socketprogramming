# receive

import socket
import hashlib  #hash library
import struct   #struct like c struct

HOST = 'localhost'  #host number
PORT = 12345 #port number
BUFFER_SIZE = 1024  #size of buffer
HEAD_STRUCT = '128sIq16s'   #128 string(file name), unsigned int(file name length), long long(file size), 32 string(md5)
info_size = struct.calcsize(HEAD_STRUCT)    #?Return the size of the struct (and hence of the bytes object produced by pack(fmt, ...)) corresponding to the format string fmt.


def cal_md5(file_path):
    with open(file_path, 'rb') as fr:   
        md5 = hashlib.md5() #open hash library's md5 object
        md5.update(fr.read())   #md5 the file
        md5 = md5.digest()   #transfer it to hex fomat
        return md5


def unpack_file_info(file_info):
    file_name, file_name_len, file_size, md5 = struct.unpack(HEAD_STRUCT, file_info)    #unpack the file_info packed with HEAD_STRUCT format
    file_name = str(file_name, encoding='utf-8')
    file_name = file_name[:file_name_len]   #correct the file_name????
    return file_name, file_size, md5


def recv_file():

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    #TCP protocal
    server_address = (HOST, PORT)   #server addrss tuples
    sock.bind(server_address)   #tie the server address with the socket
    sock.listen(1)  #wait for client at one time
    client_socket, client_address = sock.accept()   #Post: new socket with message, client_address
    print("Connected %s successfully" % str(client_address))    #print client address

    file_info_package = client_socket.recv(info_size)   #recieve a struct
    file_name, file_size, md5_recv = unpack_file_info(file_info_package)    #unpack the buffer packed by pack(fmt, ...)accoring to the string fmt.Post:tuple

    recved_size = 0 #set the receive size as 0 because have not recieved data
    with open(file_name, 'wb') as fw:   #write the file revieved in binary fomat, and the file name is same as the send edge.
        while recved_size < file_size:  #while recieve size smaller than file size
            remained_size = file_size - recved_size #set the remain size
            recv_size = BUFFER_SIZE if remained_size > BUFFER_SIZE else remained_size   #if remained size > buffer size than recieve buffer size is BUFFER_SIZE, else was remained size
            recv_file = client_socket.recv(recv_size)   #recieve was save in recv_file
            recved_size += recv_size    #update the recved_size
            fw.write(recv_file) #write the data
    md5 = cal_md5(file_name)
    print(md5, '\n' ,md5_recv)
    if md5 != md5_recv:
        print('MD5 compared fail!')
    else:
        print('Received successfully')

if __name__ == '__main__':  #if this program is imported as module this sentence will not run, else run.
    recv_file()
