import socket
import sys
import threading

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ip_addr = '127.0.0.1'
port = 8080
s.bind((ip_addr, port))

clients = []

def broadcast(msg, conn):
    try:
        msg = msg.decode().strip().encode()
        print(msg.decode())
    except:
        pass
    for client in clients:
        if client != conn:
            try:
                threading.Thread(target=sendmsg, args=(msg, client)).start()
            except:
                client.close()
                remove(client)

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


def remove(conn):
    print(conn+ 'deleted')
    if conn in clients:
        clients.remove(conn)

while True:
    try:
        msg, client = s.recvfrom(1024)
        if(client not in clients):
            clients.append(client)
        broadcast(msg, client)
    except socket.timeout:
        pass
    