from threading import Thread, Lock, Condition, Semaphore
import time

#### 3.3 - Mutex ####

#### Semaphore Implementation ####
mutex = Semaphore(1)

def threadAs(criticalSection):
    global mutex
    mutex.acquire()
    criticalSection()
    mutex.release()

def threadBs(criticalSection):
    global mutex
    mutex.acquire()
    criticalSection()
    mutex.release()

#### Monitor Implementation ####
lock = Lock()
inCriticalSectionCondition = Condition(lock)
inCriticalSection = False

def threadAm(criticalSection):
    global lock, inCriticalSectionCondition, inCriticalSection
    with lock:
	while inCriticalSection:
	    inCriticalSectionCondition.wait()
	inCriticalSection = True
	criticalSection()
	inCriticalSection = False
	inCriticalSectionCondition.notify()

def threadBm(criticalSection):
    global lock, inCriticalSectionCondition, inCriticalSection
    with lock:
	while inCriticalSection:
	    inCriticalSectionCondition.wait()
	inCriticalSection = True
    criticalSection()
    with lock:
	inCriticalSection = False
	inCriticalSectionCondition.notify()

#### Test Code ####
accountBalance = 200

if __name__ == "__main__":

    def withdraw():
	global accountBalance
	accountBalance -= 100

    def deposit():
	global accountBalance 
	accountBalance += 150

    Thread(target = threadAs, args = (withdraw,)).start()
    Thread(target = threadAs, args = (withdraw,)).start()
    Thread(target = threadBs, args = (deposit,)).start()
    Thread(target = threadBs, args = (withdraw,)).start()
    Thread(target = threadAs, args = (deposit,)).start()

    time.sleep(0.5)
    assert accountBalance == 200
    
    accountBalance = 200
    Thread(target = threadAm, args = (withdraw,)).start()
    Thread(target = threadAm, args = (withdraw,)).start()
    Thread(target = threadBm, args = (deposit,)).start()
    Thread(target = threadBm, args = (withdraw,)).start()
    Thread(target = threadAm, args = (deposit,)).start()

    time.sleep(0.5)
    assert accountBalance == 200

    print('3.3 Mutex - Passed')
