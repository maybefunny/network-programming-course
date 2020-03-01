import socket
import select
import sys
import datetime
import os

server_address = ('127.0.0.1', 5000)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(server_address)
s.listen(5)

os.makedirs('client', exist_ok=True)

input_socket = [s]

try:
    while True:
        read_ready, write_ready, exception = select.select(input_socket, [], [])
        for sock in read_ready:
            if sock == s:
                client_socket, client_addr = s.accept()
                input_socket.append(client_socket)
            else:
                # data = sock.recv(1024).decode()
                # print(str(sock.getpeername()), str(data))
                with sock.makefile('rb') as clientfile:
                    while True:
                        raw = clientfile.readline()
                        if not raw: break

                        fname = raw.strip().decode()
                        length = int(clientfile.readline())
                        print(f'downloading {fname} with length {length}')

                        path = os.path.join('client', fname)
                        os.makedirs(os.path.dirname(path), exist_ok=True)

                        f = open( path, 'wb')
                        while length:
                            chunksize = min(length, 1024)
                            chunk = clientfile.read(chunksize)
                            if not chunk: break
                            f.write(chunk)
                            length -= len(chunk)
                        else:
                            print('complete')
                            continue
                # f = open ('log', 'a')
                # f.write(str(sock.getpeername())+ ": "+ str(data)+" "+ str(datetime.datetime.now())+"\n")
                # f.close()
                # if(str(data)):
                #     sock.send(data.encode())
                # else:
                #     sock.close()
                #     input_socket.remove(sock)
except KeyboardInterrupt:
    s.close()
    sys.exit(0)