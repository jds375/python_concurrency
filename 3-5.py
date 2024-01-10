from threading import Thread, Lock, Condition, Semaphore
import time

#### 3.5 - Barrier ####

#### Semaphore Implementation ####
numThreads = 5
threadsDone = 0
barrier = Semaphore(0)
mutex = Semaphore(1)

def threadXs(beforeFunc, afterFunc):
    global numThreads, threadsDone, barrier, mutex
    beforeFunc()
    mutex.acquire()
    threadsDone += 1
    if threadsDone == numThreads:
	barrier.release()
    mutex.release()
    barrier.acquire()
    barrier.release()
    afterFunc()

#### Monitor Implementation ####
nThreads = 5
threadsFinished = 0
lock = Lock()
allThreadsCompleteCondition = Condition(lock)

def threadXm(beforeFunc, afterFunc):
    global nThreads, threadsFinished, lock, allThreadsCompleteCondition
    beforeFunc()
    with lock:
	threadsFinished += 1
	if threadsFinished == nThreads:
	    allThreadsCompleteCondition.notifyAll()
	while threadsFinished != nThreads:
	    allThreadsCompleteCondition.wait()
    afterFunc()
    
#### Test Code ####
gameStarted = False

if __name__ == "__main__":
    def joinTeam():
	global gameStarted
	time.sleep(0.2)
	assert not gameStarted

    def playGame():
	global gameStarted
	gameStarted = True

    Thread(target = threadXs, args = (joinTeam, playGame)).start()
    Thread(target = threadXs, args = (joinTeam, playGame)).start()
    Thread(target = threadXs, args = (joinTeam, playGame)).start()
    Thread(target = threadXs, args = (joinTeam, playGame)).start()
    Thread(target = threadXs, args = (joinTeam, playGame)).start()

    time.sleep(0.5)
    gameStarted = False

    Thread(target = threadXm, args = (joinTeam, playGame)).start()
    Thread(target = threadXm, args = (joinTeam, playGame)).start()
    Thread(target = threadXm, args = (joinTeam, playGame)).start()
    Thread(target = threadXm, args = (joinTeam, playGame)).start()
    Thread(target = threadXm, args = (joinTeam, playGame)).start()
    time.sleep(0.5)
    print('3.5 Barrier - Passed')
