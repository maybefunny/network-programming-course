import socket
import sys
import select
import shutil
import os
from zipfile import ZipFile

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ip_addr = '127.0.0.1'
port = 8080

msg = ''
delay = 1

s.sendto('CONNECT'.encode(), (ip_addr, port)) 

def sendFile(filename, s):
    f = open(filename, 'rb')
    i=0
    chunk = f.read(1024)
    while(chunk):
        print('sending '+str(i)+'th chunk')
        s.sendto(chunk, (ip_addr, port))
        chunk = f.read(1024)
        i+=1
    s.sendto("DONE SEND".encode(), (ip_addr, port))

def recvFile(filename, s):
    f = open('./downloads/'+str(filename), 'wb')
    chunk = s.recv(1024)
    i=0
    while(chunk):
        print('receiving '+str(i)+'th chunk')
        f.write(chunk)
        f.flush()
        chunk = s.recv(1024)
        try:
            print(chunk.decode().strip())
            if(chunk.decode().strip() == "DONE SEND"): break
        except:
            pass
        i+=1
    f.close()

def sendmsg(msg, conn):
    delay = 1
    while True:
        try:
            s.sendto(msg, conn)
            s.settimeout(delay)
        except socket.timeout:
            delay *= 2
            if delay > 2:
                return -1
        else:
            break

while True:
    sockets_list = [sys.stdin, s]

    read_socket, write_socket, error_socket = select.select(sockets_list, [], [])

    for sock in read_socket:
        if sock == s:
            msg = s.recv(2048).decode()
            splittedmsg = msg.split(' ')
            if(splittedmsg[0] == 'SEND'):
                print('file received: '+ splittedmsg[1])
                recvFile(splittedmsg[1], s)
            elif(splittedmsg[0] == 'UPTRACT'):
                print('archive received: '+ splittedmsg[1])
                recvFile(splittedmsg[1]+'.zip', s)
            else:
                print(msg)
        else:
            message = sys.stdin.readline() 
            sys.stdout.write("<You>") 
            sys.stdout.write(message)
            sys.stdout.flush()
            message = message.strip()
            splittedmsg = message.split(' ')
            if(splittedmsg[0] == 'SEND'):
                if(len(splittedmsg) < 2):
                    print('wrong usage of SEND')
                    continue
                sendmsg(message.encode(), (ip_addr, port)) 
                sendFile(splittedmsg[1], s)
            elif(splittedmsg[0] == 'UPTRACT'):
                if(len(splittedmsg) < 2):
                    print('wrong usage of UPTRACT')
                    continue
                with ZipFile(splittedmsg[1]+'.zip', 'w') as zipObj:
                    # Iterate over all the files in directory
                    for folderName, subfolders, filenames in os.walk(splittedmsg[1]):
                        for filename in filenames:
                            #create complete filepath of file in directory
                            filePath = os.path.join(folderName, filename)
                            # Add file to zip
                            zipObj.write(filePath)
                sendmsg(message.encode(), (ip_addr, port)) 
                sendFile(splittedmsg[1]+'.zip', s)
                os.remove(splittedmsg[1]+'.zip')
            else:
                sendmsg(message.encode(), (ip_addr, port)) 