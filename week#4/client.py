import socket
import sys
import select
import msvcrt

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
    if msvcrt.kbhit():
        c = msvcrt.getch()
        sys.stdout.write(str(c.decode()))
        if(c.decode() == '\r'):
            s.sendall(msg.encode())
            sys.stdout.write(str('\n'))
            sys.stdout.write('<You> '+msg+'\n')
            msg = ''
        else:
            msg = msg + str(c.decode())
        
        sys.stdout.flush() 
    # else:
    #     try:
    #         wadaw = s.recv(2048)
    #         print(wadaw)
    #     except:
    #         pass
s.close()