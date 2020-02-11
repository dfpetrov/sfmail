import threading
import random
import time

def worker(i):
    interval = random.randint(0,10)
    time.sleep(interval)
    print('Worker # % s is sleeping for % s seconds' % (str(i), str(interval)))


threads = []
for i in range(5):
    t = threading.Thread(target=worker, args=(i, ))
    threads.append(t)
    print("Starting % i thread" % i)
    t.start()

for t in threads:
    t.join()