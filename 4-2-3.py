from threading import Thread, Lock, Condition, Semaphore
import time
import Queue

#### 4.2.3 - Reader Writer Starvation ####

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
noReaders = Semaphore(1)
turnstile = Semaphore(1)

def readerS(r):
    global readSwitch, noReaders, turnstile
    turnstile.acquire()
    turnstile.release()
    readSwitch.lock(noReaders)
    r()
    readSwitch.unlock(noReaders)    

def writerS(w):
    global readSwitch, turnstile
    turnstile.acquire()
    noReaders.acquire()
    w()
    noReaders.release()
    turnstile.release()

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

    print('4.2.3 Reader Writer Starvation - Passed')

