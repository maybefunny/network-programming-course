import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

addr = input('Server addr: ')
port = input('Server port: ')
server_address = (addr, int(port))
sock = s.connect(server_address)

filename = input('Filename: ')
s.send(filename.encode())

f = open(filename, 'rb')
chunk = f.read(1024)
while(chunk):
    s.send(chunk)
    chunk = f.read(1024)

# sock.send('test')

s.close()