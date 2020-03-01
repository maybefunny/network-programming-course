import socket
import select
import queue
from threading import Thread
from time import sleep
from random import randint
import sys

class ProcessThread(Thread):
    def __init__(self):
        super(ProcessThread, self).__init__()
        self.running = True
        self.q = queue.Queue()
    def add(self, data):
        self.q.put(data)

    def stop(self):
        self.running = False
    def run(self):
        q = self.q
        while self.running:
            try:
                # block for 1 second only:
                value = q.get(block=True, timeout=1)
                process(value[0], value[1])
            except queue.Empty:
                sys.stdout.write('.')
                sys.stdout.flush()
            #
        if not q.empty():
            print ("Elements left in the queue:")
        while not q.empty():
            print (q.get())
t = ProcessThread()
t.start()

def process(value, client):
    """
    Implement this. Do something useful with the received data.
    """
    f = open('socket.log', 'a')
    f.write(value.decode())
    print(value.decode())
    client.sendall(value)
    sleep(randint(1,5)) # emulating processing time

def main():
    s = socket.socket() # Create a socket object
    host = 'localhost' # Get local machine name
    port = 5001 # Reserve a port for your service.
    s.bind((host, port)) # Bind to the port
    print ("Listening on port {p}...".format(p=port))

    s.listen(5) # Now wait for client connection.
    while True:
        try:
            client, addr = s.accept()
            ready = select.select([client,],[], [],2)
            if ready[0]:
                data = client.recv(4096)
            print(data)
            t.add([data, client])
            # client.sendall(data)
        except KeyboardInterrupt:
            print
            print("Stop.")
            break
        except socket.error as msg:
            print("Socket error! %s" % msg)
            break
        #
    cleanup()

def cleanup():
    t.stop()
    t.join()

#########################################################

if __name__ == "__main__":
    main()