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

                        f = open ('result.txt', 'a')
                        try:
                            res = eval(raw.decode().strip())
                        except ZeroDivisionError:
                            res = 'Division by zero'
                        f.writelines(str(res)+'\n')
                        f.close()
                # if(str(data)):
                #     sock.send(data.encode())
                # else:
                #     sock.close()
                #     input_socket.remove(sock)
except KeyboardInterrupt:
    s.close()
    sys.exit(0)