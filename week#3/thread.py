import threading
import datetime
import logging

logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s',)

class ThreadClass(threading.Thread):
    def __init__(self, num):
        threading.Thread.__init__(self)
        self.num = num
    def run(self):
        # now = datetime.datetime.now()
        # print(self.getName() + 'Says Hello World at time: ' + str(now) + '\n')
        logging.debug(str(self.num) + 'running')

def func(num):
    print('Worker: '+ str(num))

threads = []
for i in range(5):
    # t = threading.Thread(target=func, args=(i,))
    # threads.append(t)
    # t.start()

    t = ThreadClass(i)
    t.start()