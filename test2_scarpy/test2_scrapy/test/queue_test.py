import threading
from queue import Queue
import time
import random

q1 = Queue()
# q2 = Queue()
# q3 = Queue()

def warn1(q):
    while True:
        data = q.get()
        #time.sleep(1)
        time.sleep(random.random())
        print ('w1',data)
        q.task_done()
    pass

def warn2(q):
    while True:
        data = q.get()
        #time.sleep(1)
        time.sleep(random.random())
        print ('w2',data)
        q.task_done()
    pass

def warn3(q):
    while True:
        data = q.get()
        #time.sleep(2)
        time.sleep(random.random())
        print ('w3',data)
        q.task_done()
    pass

task_func = [(warn1, q1),(warn2, q1),(warn3, q1)]
for f, q in task_func:
    t = threading.Thread(target=f, args=(q,))
    #添加守护进程 当队列任务全部完成时 主线程退出 子线程退出
    t.setDaemon(True)
    t.start()

if __name__ == '__main__':
    task_list = range(30)
    for i in task_list:
        q1.put(i)
        #q2.put(i)
        #q3.put(i)
    #等待队列任务全部完成
    #q1.join()
    # q2.join()
    # q3.join()
    #time.sleep(1)
    #print ('全部结束')
    while True:
        print (q1.qsize())
        time.sleep(1)
