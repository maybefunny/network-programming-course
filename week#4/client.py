import socket
import sys
import select

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip_addr = '127.0.0.1'
port = 8080
s.connect((ip_addr, port))

while True:
    sockets_list = [sys.stdin, s]

    read_socket, write_socket, error_socket = select.select(sockets_list, [], [])

    for sock in read_socket:
        if sock == s:
            msg = s.recv(2048)
            print(msg)
        else:
            msg = sys.stdin.readline()
            s.sendall(msg.encode())
            sys.stdout.write('<You> ')
            sys.stdout.write(msg)
            sys.stdout.flush()

s.close()