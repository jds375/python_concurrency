from threading import Thread, Lock, Condition, Semaphore
import time
import Queue

#### 4.2.7 - Reader Writer Starvation Priority ####

#### Semaphore Implementation ####
class Lightswitch:
    def __init__(self):
	self.counter = 0
	self.mutex = Semaphore(1)

    def lock(self, semaphore):
	self.mutex.acquire()
	self.counter += 1
	if self.counter == 1:
	    semaphore.acquire()
	self.mutex.release()

    def unlock(self, semaphore):
	self.mutex.acquire()
	self.counter -= 1
	if self.counter == 0:
	    semaphore.release()
	self.mutex.release()

readSwitch = Lightswitch()
writeSwitch = Lightswitch()
canRead = Semaphore(1)
canWrite = Semaphore(1)

def readerS(r):
    global readSwitch, writerSwitch, canRead, canWrite, mutex
    canRead.acquire()
    readSwitch.lock(canWrite)
    canRead.release()
    r()
    readSwitch.unlock(canWrite)

def writerS(w):
    global readSwitch, writerSwitch, canRead, canWrite, mutex
    writeSwitch.lock(canRead)
    canWrite.acquire()
    w()
    canWrite.release()
    writeSwitch.unlock(canRead)


#### Monitor Implementation ####
lock = Lock()
nReaders = 0
writersReady = 0
writersTurnCondition = Condition(lock)
canWriteCondition = Condition(lock)

def readerM(r):
    global lock, nReaders, canWriteCondition, writersReady, writersTurnCondition
    with lock:
	while writersReady > 0:
	    writersTurnCondition.wait()
	nReaders += 1
    r()
    with lock:
	nReaders -= 1
	if nReaders == 0:
	    canWriteCondition.notify()
	
def writerM(w):
    global lock, nReaders, canWriteCondition, writersReady, writersTurnCondition
    with lock:
	writersReady += 1
	while nReaders > 0:
	    canWriteCondition.wait()
	w()
	writersReady -= 1
	writersTurnCondition.notifyAll()

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

    print('4.2.7 Reader Writer Starvation Priority - Passed')


