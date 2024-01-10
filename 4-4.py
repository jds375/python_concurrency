from threading import Thread, Lock, Condition, Semaphore
import time
import Queue

#### 4.4 - Dining Philosophers####

#### Helper Functions ####
numPhilosophers = 5
iters = 100

def left(i):
    return i

def right(i):
    return (i + 1) % numPhilosophers

def think():
    time.sleep(0.002)

def eat():
    time.sleep(0.01)

def philosopherFunction(i, g, p):
    global iters
    for x in range(iters):
	think()
	g(i)
	eat()
	p(i)

#### Semaphore Solution ####
forkAccess = Semaphore(numPhilosophers - 1)
forks = [Semaphore(1) for x in range(0, numPhilosophers)]

def getForksS(i):
    global forkAccess, forks
    forkAccess.acquire()
    forks[right(i)].acquire()
    forks[left(i)].acquire()

def putForksS(i):
    global forkAccess, forks
    forks[right(i)].release()
    forks[left(i)].release()
    forkAccess.release()

#### Monitor Solution ####
atTable = 0
lock = Lock()
tableBusyCondition = Condition(lock)
forkFreeCondition = [Condition(lock) for x in range(0, numPhilosophers)]
forkFree = [True] * 5

def getForksM(i):
    global lock, atTable, lock, tableBusyCondition, forkFreeCondition, forkFree
    with lock:
        while atTable == (numPhilosophers - 1):
            tableBusyCondition.wait()
        atTable += 1
        while not forkFree[right(i)]:
            forkFreeCondition[right(i)].wait()
        forkFree[right(i)] = False
        while not forkFree[left(i)]:
            forkFreeCondition[left(i)].wait()
        forkFree[left(i)] = False
    
def putForksM(i):
    global lock, atTable, lock, tableBusyCondition, forkFreeCondition, forkFree
    with lock:
        atTable -= 1
        forkFree[right(i)] = True
        forkFreeCondition[right(i)].notify()
        forkFree[left(i)] = True
        forkFreeCondition[left(i)].notify()
        tableBusyCondition.notify()

	

#### Test Code ####
if __name__ == "__main__":

    Thread(target = philosopherFunction, args = (0, getForksS, putForksS)).start()
    Thread(target = philosopherFunction, args = (1, getForksS, putForksS)).start()
    Thread(target = philosopherFunction, args = (2, getForksS, putForksS)).start()
    Thread(target = philosopherFunction, args = (3, getForksS, putForksS)).start()
    Thread(target = philosopherFunction, args = (4, getForksS, putForksS)).start()

    Thread(target = philosopherFunction, args = (0, getForksM, putForksM)).start()
    Thread(target = philosopherFunction, args = (1, getForksM, putForksM)).start()
    Thread(target = philosopherFunction, args = (2, getForksM, putForksM)).start()
    Thread(target = philosopherFunction, args = (3, getForksM, putForksM)).start()
    Thread(target = philosopherFunction, args = (4, getForksM, putForksM)).start()

    time.sleep(20)
    print('4.4 Dining Philosophers - Passed')
