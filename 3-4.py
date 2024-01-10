from threading import Thread, Lock, Condition, Semaphore
import time

#### 3.4 - Multiplex ####

#### Semaphore Implementation ####
freeSpotsSemaphore = Semaphore(5) # Number allowed in critical section

def threadXs(criticalSection):
    global freeSpotsSemaphore
    freeSpotsSemaphore.acquire()
    criticalSection()
    freeSpotsSemaphore.release()

#### Monitor Implementation ####
lock = Lock()
freeSpotsCondition = Condition(lock)
numFreeSpots = 5 # Number allowed in critical section

def threadXm(criticalSection):
    global lock, freeSpotsCondition, numFreeSpots
    with lock:
	while numFreeSpots <= 0:
	    freeSpotsCondition.wait()
	numFreeSpots -= 1
    criticalSection()
    with lock:
	numFreeSpots += 1
	freeSpotsCondition.notify()

#### Test Code ####
roomSize = 5 # Number allowed in room (critical section)

if __name__ == "__main__":

    timeStart = time.time()
    def enterRoom():
	time.sleep(.2)

    Thread(target = threadXs, args = (enterRoom,)).start()
    Thread(target = threadXs, args = (enterRoom,)).start()
    Thread(target = threadXs, args = (enterRoom,)).start()
    Thread(target = threadXs, args = (enterRoom,)).start()
    Thread(target = threadXs, args = (enterRoom,)).start()
    Thread(target = threadXs, args = (enterRoom,)).start()
    Thread(target = threadXs, args = (enterRoom,)).start()

    Thread(target = threadXm, args = (enterRoom,)).start()
    Thread(target = threadXm, args = (enterRoom,)).start()
    Thread(target = threadXm, args = (enterRoom,)).start()
    Thread(target = threadXm, args = (enterRoom,)).start()
    Thread(target = threadXm, args = (enterRoom,)).start()
    Thread(target = threadXm, args = (enterRoom,)).start()
    Thread(target = threadXm, args = (enterRoom,)).start()

    time.sleep(.5)
    print('3.4 Multiplex - Passed')
