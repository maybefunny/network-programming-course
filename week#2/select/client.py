import socket
import sys
import os

server_address = ('127.0.0.1', 5000)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock = s.connect(server_address)

try:
    while True:
        fname = input()
        f = open(fname, 'r')
        while True:
            operation = f.readline()
            if not operation:
                s.close()
                break
            s.sendall(operation.encode())
        # s.send(data.encode())
        # data = s.recv(1024).decode()
        # print(str(data))
except KeyboardInterrupt:
    s.close()
    sys.exit(0)