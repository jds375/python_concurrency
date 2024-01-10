from threading import Thread, Lock, Condition, Semaphore
import time

#### 3.7.3 - Exclusive Queue ####

#### Semaphore Implementation ####
numA = 0
numB = 0
mutex = Semaphore(1)
aQueue = Semaphore(0)
bQueue = Semaphore(0)
rendezvous = Semaphore(0)

def aJoins(aExecute):
    global numA, numB, mutex, aQueue, bQueue, rendezvous
    mutex.acquire()
    if numB > 0:
	numB -= 1
	bQueue.release()
    else:
	numA += 1
	mutex.release()
	aQueue.acquire()
    aExecute()
    rendezvous.acquire()
    mutex.release()

def bJoins(bExecute):
    global numA, numB, mutex, aQueue, bQueue, rendezvous
    mutex.acquire()
    if numA > 0:
	numA -= 1
	aQueue.release()
    else:
	numB += 1
	mutex.release()
	bQueue.acquire()
    bExecute()
    rendezvous.release()

#### Monitor Implementation ####
lock = Lock()
aWent = False
bWent = False
aWentCondition = Condition(lock)
bWentCondition = Condition(lock)

def aJoinm(aExecute):
    global lock, aWent, bWent, aWentCondition, bWentCondition
    with lock:
	while aWent:
	    bWentCondition.wait()
	aExecute()
	aWent = True
	bWent = False
	aWentCondition.notify()

def bJoinm(bExecute):
    global lock, aWent, bWent, aWentCondition, bWentCondition
    with lock:
	while bWent:
	    aWentCondition.wait() 
	bExecute()
	bWent = True
	aWent = False
	bWentCondition.notify()

#### Test Code ####
testLock = Lock()
numAInARow = 0

if __name__ == "__main__":
    def aExecute():
	global testLock, numAInARow
	time.sleep(0.05)
	with testLock:
	    numAInARow += 1
	    assert -1 <= numAInARow <= 1

    def bExecute():
	global testLock, numAInARow
	time.sleep(0.05)
	with testLock:
	    numAInARow -= 1
	    assert -1 <= numAInARow <= 1

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

    print('3.7.3 Exclusive Queue - Passed')

