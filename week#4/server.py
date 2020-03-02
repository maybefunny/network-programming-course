import socket
import select
import sys
import threading

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
ip_addr = '127.0.0.1'
port = 8080
s.bind((ip_addr, port))
s.listen(100)
clients = []

def clientthread(conn, addr):
    while True:
        try:
            msg = conn.recv(2048)
            if msg:
                msg_to_send = '<' + addr[0] + '> ' + msg.decode()
                print(msg_to_send)
                broadcast(msg, conn)
            else:
                remove(conn)
        except:
            continue

def broadcast(msg, conn):
    for client in clients:
        if client != conn:
            try:
                print(msg, client)
                client.send(msg.encode())
            except:
                client.close()
                remove(client)

def remove(conn):
    print(conn+ 'deleted')
    if conn in clients:
        clients.remove(conn)

while True:
    conn, addr = s.accept()
    clients.append(conn)
    print(addr[0] + ' connected')
    threading.Thread(target=clientthread, args=(conn, addr)).start()

conn.close()
    