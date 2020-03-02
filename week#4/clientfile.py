# Python program to implement client side of chat room. 
import socket 
import select 
import sys 

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
if len(sys.argv) != 3: 
	print("Correct usage: script, IP address, port number")
	exit() 
IP_address = str(sys.argv[1]) 
Port = int(sys.argv[2]) 
server.connect((IP_address, Port)) 

while True: 

	# maintains a list of possible input streams 
	sockets_list = [sys.stdin, server] 

	read_sockets,write_socket, error_socket = select.select(sockets_list,[],[]) 

	for socks in read_sockets: 
		if socks == server:
			print(socks)
			filename = socks.recv(1024).decode() 
			print(filename)
			f = open('./upload/'+str(filename), 'wb')
			i=0
			chunk = socks.recv(1024)
			while(chunk):
				print('receiving '+str(i)+'th chunk')
				print(chunk.decode())
				f.write(chunk)
				f.flush()
				chunk = socks.recv(1024)
			f.close()
			print('done')
		else: 
			message = sys.stdin.readline() 
			server.send(message.encode()) 
			sys.stdout.write("<You>") 
			sys.stdout.write(message) 
			sys.stdout.flush() 
			f = open(message[0:-1], 'rb')
			i=0
			chunk = f.read(1024)
			while(chunk):
				print('sending '+str(i)+'th chunk')
				server.send(chunk)
				chunk = f.read(1024)
server.close() 
