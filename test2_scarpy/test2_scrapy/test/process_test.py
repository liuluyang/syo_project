from multiprocessing import Pool, Manager
import os, time, random

def long_time_task(name, d):
    while True:
        print('Run task %s (%s)...' % (name, os.getpid()))
        start = time.time()
        time.sleep(2)#random.random() * 3)
        end = time.time()
        if name==3:
            int('23.8')
            #raise #AttributeError('name error')
        print('Task %s runs %0.2f seconds.' % (name, (end - start)))

def error(e):
    print ('子进程中有异常')
    d['s'] = 1
    exit()
    raise
    #print (e)
    #print ('error')

if __name__=='__main__':
    print('Parent process %s.' % os.getpid())
    d = Manager().dict()
    p = Pool(5)
    for i in range(5):
        result = p.apply_async(long_time_task, args=(i,d), error_callback=error)
    print('Waiting for all subprocesses done...')
    # p.close()
    # p.join()
    while True:
        print (p, time.time())
        print (d)
        if d:
            #exit()
            p.terminate()
        time.sleep(2)
    #print('All subprocesses done.')