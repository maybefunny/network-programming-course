import threading
import queue
import time

myQueue = queue.Queue()

class count_stuff(threading.Thread):
    def __init__(self, start_num, end, q):
        self.num = start_num
        self.end = end
        self.q = q
        threading.Thread.__init__(self)

    def run(self):
        while True:
            if self.num != self.end:
                self.num += 1
                self.q.put(self.num)
                time.sleep(5)
            else:
                break

myThread = count_stuff(1,5, myQueue)
myThread.start()

while not myQueue.empty():
    val = myQueue.get()
    print('outputting: ' + str(val))
    time.sleep(2)