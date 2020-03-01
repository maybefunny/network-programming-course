import socket
import sys

server_address = ('localhost', 5000)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(server_address)
s.listen(5)

try:
    while(True):
        sock, client_addr = s.accept()
        data = sock.recv(65536)
        sock.send(data)
        print(str(data.decode()))
        sock.close()
except KeyboardInterrupt:
    s.close()
    sys.exit(0)