from threading import Thread, Lock, Condition, Semaphore
import time
import Queue

#### 4.1 - Producer Consumer ####

#### Semaphore Implementation ####
mutex = Semaphore(1)
buff = []
itemAvailable = Semaphore(0)

def produceS(f):
    global mutex, buff, itemAvailable
    item = f()
    mutex.acquire()
    buff.append(item)
    mutex.release()
    itemAvailable.release()

def consumeS(f):
    global mutex, buff, itemAvailable
    itemAvailable.acquire()
    item = None
    mutex.acquire()
    item = buff.pop(0)
    mutex.release()
    f(item)

#### Monitor Implementation ####
lst = []
lock = Lock()
spaceAvailableCondition = Condition(lock)

def produceM(f):
    global lst, lock, spaceAvailableCondition
    item = f()
    with lock:
	lst.append(item)
	spaceAvailableCondition.notify()

def consumeM(f):
    global lst, lock, spaceAvailableCondition
    item = None
    with lock:
	while len(lst) <= 0:
	    spaceAvailableCondition.wait()
	item = lst.pop(0)
    f(item)

#### Test Code ####
tlock = Lock()
count = 0

if __name__ == "__main__":
    def p():
	time.sleep(0.1)
	return 'data'
    
    def c(item):
	global tlock, count
	with tlock:
	    count += 1
 
    Thread(target = consumeS, args = (c,)).start()
    Thread(target = produceS, args = (p,)).start()
    Thread(target = consumeS, args = (c,)).start()
    time.sleep(0.2)
    assert count == 1
    Thread(target = produceS, args = (p,)).start()
    Thread(target = produceS, args = (p,)).start()
    Thread(target = produceS, args = (p,)).start()
    Thread(target = produceS, args = (p,)).start()
    Thread(target = consumeS, args = (c,)).start()
    Thread(target = consumeS, args = (c,)).start()
    Thread(target = consumeS, args = (c,)).start()
    time.sleep(0.5)
    assert count == 5

    count = 0
    Thread(target = consumeM, args = (c,)).start()
    Thread(target = produceM, args = (p,)).start()
    Thread(target = consumeM, args = (c,)).start()
    time.sleep(0.2)
    assert count == 1
    Thread(target = produceM, args = (p,)).start()
    Thread(target = produceM, args = (p,)).start()
    Thread(target = produceM, args = (p,)).start()
    Thread(target = produceM, args = (p,)).start()
    Thread(target = consumeM, args = (c,)).start()
    Thread(target = consumeM, args = (c,)).start()
    Thread(target = consumeM, args = (c,)).start()
    time.sleep(0.5)
    assert count == 5

    print('4.1 Producer Consumer - Passed')
