from threading import Thread, Lock, Condition, Semaphore
import time
import Queue

#### 3.8 - FIFO Thread Queue ####

#### Semaphore Implementation ####
class FifoS:
    def __init__(self):
	self.sharedSemaphore = Semaphore(0)
	
    def wait(self):
	self.sharedSemaphore.acquire()

    def signal(self):
	self.sharedSemaphore.release()

#### Monitor Implementation ####
class FifoM:
    def __init__(self):
	self.lock = Lock()
	self.numSignals = 0
	self.signalRequestCondition = Condition(self.lock)

    def wait(self):
	with self.lock:
	    while self.numSignals <= 0:
		self.signalRequestCondition.wait()
	    self.numSignals -= 1

    def signal(self):
	with self.lock:
	    self.numSignals += 1
	    self.signalRequestCondition.notify()

#### Test Code ####
lock = Lock()
count = 0

if __name__ == "__main__":
    def incCounter(q):
	global lock, count
	q.wait()
	with lock:
	    count += 1

    fifoS = FifoS()
    fifoM = FifoM()

    Thread(target = incCounter, args = (fifoS,)).start()
    Thread(target = incCounter, args = (fifoS,)).start()
    Thread(target = incCounter, args = (fifoS,)).start()
    assert count == 0
    fifoS.signal()
    fifoS.signal()
    time.sleep(0.2)
    assert count == 2
    fifoS.signal()

    time.sleep(0.1)
    count = 0

    Thread(target = incCounter, args = (fifoM,)).start()
    Thread(target = incCounter, args = (fifoM,)).start()
    Thread(target = incCounter, args = (fifoM,)).start()
    assert count == 0
    fifoM.signal()
    fifoM.signal()
    time.sleep(0.2)
    assert count == 2
    fifoM.signal()
    
    print('3.8 FIFO Queue - Passed')

