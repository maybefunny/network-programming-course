import socket
import sys
import select

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ip_addr = '127.0.0.1'
port = 8080

msg = ''
delay = 1

s.sendto('CONNECT'.encode(), (ip_addr, port)) 


while True:
    sockets_list = [sys.stdin, s]

    read_socket, write_socket, error_socket = select.select(sockets_list, [], [])

    for sock in read_socket:
        if sock == s:
            msg = s.recv(2048).decode()
            print(msg)
        else:
            message = sys.stdin.readline() 
            s.sendto(message.encode(), (ip_addr, port)) 
            sys.stdout.write("<You>") 
            sys.stdout.write(message)
            sys.stdout.flush()

