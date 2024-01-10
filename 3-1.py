from threading import Thread, Lock, Condition, Semaphore
import time

#### 3.1 - Signaling ####

#### Semaphore Implementation ####
aDoneSemaphore = Semaphore(0)

def threadAs(statement):
    global aDoneSemaphore
    statement()
    aDoneSemaphore.release()

def threadBs(statement):
    global aDoneSemaphore
    aDoneSemaphore.acquire()
    statement()
 
#### Monitor Implementation ####
signalLock = Lock()
aDoneCondition = Condition(signalLock)
aDone = False

def threadAm(statement):
    global signalLock, aDoneCondition, aDone
    with signalLock:
	statement()
	aDone = True
	aDoneCondition.notify()

def threadBm(statement):
    global signalLock, aDoneCondtion, aDone
    with signalLock:
	while not aDone:
	    aDoneCondition.wait()
	statement()

#### Test Code ####
rocketsReady = False

if __name__ == "__main__":
    def prepareRockets():
	global rocketsReady
	time.sleep(0.2)
	rocketsReady = True

    def fireRockets():
	global rocketsReady
	assert rocketsReady
	#fire rocket now

    Thread(target = threadAs, args = (prepareRockets,)).start()
    Thread(target = threadBs, args = (fireRockets,)).start()
    
    Thread(target = threadAm, args = (prepareRockets,)).start()
    Thread(target = threadBm, args = (fireRockets,)).start()
	
    print('3.1 Signaling - Passed')
