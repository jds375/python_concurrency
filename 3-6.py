from threading import Thread, Lock, Condition, Semaphore
import time

#### 3.6 - Reusable Barrier ####

#### Semaphore Implementation ####
numThreads = 5
threadsDone = 0
mutex = Semaphore(1)
turnstile1 = Semaphore(0)
turnstile2 = Semaphore(1)

def threadXs(beforeFunc, afterFunc):
    global numThreads, threadsDone, turnstile1, turnstile2, mutex
    beforeFunc()
    mutex.acquire()
    threadsDone += 1
    if threadsDone == numThreads:
	turnstile2.acquire()
	turnstile1.release()
    mutex.release()
    turnstile1.acquire()
    turnstile1.release()
    afterFunc()
    mutex.acquire()
    threadsDone -= 1
    if threadsDone == 0:
	turnstile1.acquire()
	turnstile2.release()
    mutex.release()
    turnstile2.acquire()
    turnstile2.release()

#### Monitor Implementation ####
nThreads = 5
threadsFinished = 0
threadsCompleted = 0
lock = Lock()
turnstile1Condition = Condition(lock)
turnstile2Condition = Condition(lock)

def threadXm(beforeFunc, afterFunc):
    global nThreads, threadsFinished, threadsCompleted, lock, turnstile1Condition, turnstile2Condition
    beforeFunc()
    with lock:
        threadsFinished += 1
        if threadsFinished == nThreads:
            threadsCompleted = 0
            turnstile1Condition.notifyAll()
        else:
            while threadsFinished != nThreads:
                turnstile1Condition.wait()
    afterFunc()
    with lock:
        threadsCompleted += 1
        if threadsCompleted == 5:
            threadsFinished = 0
            turnstile2Condition.notifyAll()
        else:
            while threadsCompleted != nThreads:
                turnstile2Condition.wait()
    
#### Test Code ####
gameStarted = False

if __name__ == "__main__":
    def joinTeam():
	global gameStarted
	time.sleep(0.1)
	assert not gameStarted

    def playGame():
	global gameStarted
	gameStarted = True
    
    for i in range(0,3):
	Thread(target = threadXs, args = (joinTeam, playGame)).start()
	Thread(target = threadXs, args = (joinTeam, playGame)).start()
	Thread(target = threadXs, args = (joinTeam, playGame)).start()
	Thread(target = threadXs, args = (joinTeam, playGame)).start()
	Thread(target = threadXs, args = (joinTeam, playGame)).start()
    
	time.sleep(0.3)
	gameStarted = False
    
    for i in range(0,1):
	Thread(target = threadXm, args = (joinTeam, playGame)).start()
	Thread(target = threadXm, args = (joinTeam, playGame)).start()
	Thread(target = threadXm, args = (joinTeam, playGame)).start()
	Thread(target = threadXm, args = (joinTeam, playGame)).start()
	Thread(target = threadXm, args = (joinTeam, playGame)).start()
	time.sleep(0.3)
	gameStarted = False

    print('3.6 Reusable Barrier - Passed')

