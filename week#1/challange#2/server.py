import socket
import sys

server_address = ('localhost', 5001)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(server_address)
s.listen(5)

try:
    while(True):
        sock, client_addr = s.accept()
        filename = sock.recv(1024).decode()
        f = open('./upload/'+str(filename), 'wb')
        # while True:
        chunk = sock.recv(1024)
        while(chunk):
            f.write(chunk)
            chunk = sock.recv(1024)
        f.close()
        sock.close()
except KeyboardInterrupt:
    s.close()
    sys.exit(0)