from threading import Thread, Lock, Condition, Semaphore
import time

#### 3.7 - Queue ####

#### Semaphore Implementation ####
aQueue = Semaphore(0)
bQueue = Semaphore(0)

def aJoins(aExecute):
    global aQueue, bQueue
    bQueue.release()
    aQueue.acquire()
    aExecute()

def bJoins(bExecute):
    global aQueue, bQueue
    aQueue.release()
    bQueue.acquire()
    bExecute()

#### Monitor Implementation ####
lock = Lock()
aQueueSize = 0
bQueueSize = 0
aQueueEmptyCondition = Condition(lock)
bQueueEmptyCondition = Condition(lock)

def aJoinm(aExecute):
    global lock, aQueueSize, bQueueSize, aQueueEmptyCondition, bQueueEmptyCondition
    with lock:
	aQueueSize += 1
	while bQueueSize == 0:
	    bQueueEmptyCondition.wait()
	aQueueEmptyCondition.notify()
	bQueueSize -= 1
    aExecute()

def bJoinm(bExecute):
    global lock, aQueueSize, bQueueSize, aQueueEmptyCondition, bQueueEmptyCondition
    with lock:
	bQueueSize += 1
	while aQueueSize == 0:
	    aQueueEmptyCondition.wait()
	bQueueEmptyCondition.notify()
	aQueueSize -= 1
    bExecute()

#### Test Code ####
if __name__ == "__main__":
    def aExecute():
	time.sleep(0.1)

    def bExecute():
	time.sleep(0.1)

    Thread(target = aJoins, args = (aExecute,)).start()
    Thread(target = bJoins, args = (bExecute,)).start()
    Thread(target = aJoins, args = (aExecute,)).start()
    Thread(target = bJoins, args = (bExecute,)).start()
    Thread(target = aJoins, args = (aExecute,)).start()
    Thread(target = bJoins, args = (bExecute,)).start()
    Thread(target = bJoins, args = (bExecute,)).start()
    Thread(target = aJoins, args = (aExecute,)).start()
    Thread(target = bJoins, args = (bExecute,)).start()
    Thread(target = aJoins, args = (aExecute,)).start()

    time.sleep(0.5)

    Thread(target = aJoinm, args = (aExecute,)).start()
    Thread(target = bJoinm, args = (bExecute,)).start()
    Thread(target = aJoinm, args = (aExecute,)).start()
    Thread(target = bJoinm, args = (bExecute,)).start()
    Thread(target = aJoinm, args = (aExecute,)).start()
    Thread(target = bJoinm, args = (bExecute,)).start()
    Thread(target = bJoinm, args = (bExecute,)).start()
    Thread(target = aJoinm, args = (aExecute,)).start()
    Thread(target = bJoinm, args = (bExecute,)).start()
    Thread(target = aJoinm, args = (aExecute,)).start()

    time.sleep(0.5)

    print('3.7 Queue - Passed')

