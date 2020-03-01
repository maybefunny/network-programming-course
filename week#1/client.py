import socket

server_address = ('localhost', 5001)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock = s.connect(server_address)

s.send(input().encode())
print(s.recv(1024).decode())
s.close()


# try:
    # while(True):
        # sock, client_addr = s.accept()
        # data = sock.recv(65536).decode()
        # print(str(data))
        # sock.close()
# except KeyboardInterrupt:
    # s.close()
    # exit(0)