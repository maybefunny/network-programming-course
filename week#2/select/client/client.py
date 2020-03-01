import socket
import sys
import os

server_address = ('127.0.0.1', 5000)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock = s.connect(server_address)

try:
    while True:
        data = input()
        for path,dirs,files in os.walk(data):
            for file in files:
                fname = os.path.join(path,file)
                relpath = os.path.relpath(fname, data)
                fsize = os.path.getsize(fname)

                print(f'sending (relpath)')

                f = open(fname, 'rb')
                s.sendall(relpath.encode() + b'\n')
                s.sendall(str(fsize).encode() + b'\n')

                while True:
                    chunk = f.read(1024)
                    if not chunk: break
                    s.sendall(chunk)
        print('done')
        # s.send(data.encode())
        # data = s.recv(1024).decode()
        # print(str(data))
except KeyboardInterrupt:
    s.close()
    sys.exit(0)