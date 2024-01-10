from threading import Thread, Lock, Condition, Semaphore
import time
import Queue

#### 4.2 - Reader Writer ####

#### Semaphore Implementation ####
mutex = Semaphore(1)
writeSemaphore = Semaphore(1)
numReaders = 0

def readerS(r):
    global mutex, writeSemaphore, numReaders
    mutex.acquire()
    numReaders += 1
    if numReaders == 1:
	writeSemaphore.acquire()
    mutex.release()
    r()
    mutex.acquire()
    numReaders -= 1
    if numReaders == 0:
	writeSemaphore.release()
    mutex.release()

def writerS(w):
    global mutex, writeSemaphore, numReaders
    writeSemaphore.acquire()
    w()
    writeSemaphore.release()

#### Monitor Implementation ####
lock = Lock()
nReaders = 0
canWriteCondition = Condition(lock)

def readerM(r):
    global lock, nReaders, canWriteCondition
    with lock:
	nReaders += 1
    r()
    with lock:
	nReaders -= 1
	if nReaders == 0:
	    canWriteCondition.notify()
	
def writerM(w):
    global lock, nReaders, canWriteCondition
    with lock:
	while nReaders > 0:
	    canWriteCondition.wait()
	w()

#### Test Code ####
data = 'hello, my name is bob'

if __name__ == "__main__":
    def r():
	global data
	time.sleep(0.1)

    def w():
	global data
	data += '.'

    Thread(target = writerS, args = (w,)).start()
    time.sleep(0.05)
    assert data == 'hello, my name is bob.'
    Thread(target = readerS, args = (r,)).start()
    Thread(target = readerS, args = (r,)).start()
    Thread(target = readerS, args = (r,)).start()
    Thread(target = writerS, args = (w,)).start()
    assert data == 'hello, my name is bob.'
    Thread(target = readerS, args = (r,)).start()
    time.sleep(0.3)
    assert data == 'hello, my name is bob..'

    data = 'hello, my name is bob'

    Thread(target = writerM, args = (w,)).start()
    time.sleep(0.05)
    assert data == 'hello, my name is bob.'
    Thread(target = readerM, args = (r,)).start()
    Thread(target = readerM, args = (r,)).start()
    Thread(target = readerM, args = (r,)).start()
    Thread(target = writerM, args = (w,)).start()
    assert data == 'hello, my name is bob.'
    Thread(target = readerM, args = (r,)).start()
    time.sleep(0.3)
    assert data == 'hello, my name is bob..'

    print('4.2 Reader Writer - Passed')
