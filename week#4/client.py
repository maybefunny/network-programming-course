import socket
import sys
import select

# while True:
#    if msvcrt.kbhit():
#       print("you pressed"+str(msvcrt.getch())+"so now i will quit")
#       done = True

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip_addr = '127.0.0.1'
port = 8080
s.connect((ip_addr, port))

msg = ''
while True:
    sockets_list = [sys.stdin, s]

    read_socket, write_socket, error_socket = select.select(sockets_list, [], [])

    for sock in read_socket:
        if sock == s:
            msg = s.recv(2048).decode()
            print(msg)
        else:
            message = sys.stdin.readline() 
            s.send(message.encode()) 
            sys.stdout.write("<You>") 
            sys.stdout.write(message)
            sys.stdout.flush()
    # else:
    #     try:
    #         wadaw = s.recv(2048)
    #         print(wadaw)
    #     except:
    #         pass
s.close()