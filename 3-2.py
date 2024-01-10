from threading import Thread, Lock, Condition, Semaphore
import time

#### 3.2 - Rendezvous ####

#### Semaphore Implementation ####
a1DoneSemaphore = Semaphore(0)
b1DoneSemaphore = Semaphore(0)

def threadAs(statement1, statement2):
    global a1DoneSemaphore, b1DoneSemaphore
    statement1()
    a1DoneSemaphore.release()
    b1DoneSemaphore.acquire()
    statement2()

def threadBs(statement1, statement2):
    global a1DoneSemaphore, b1DoneSemaphore
    statement1()
    b1DoneSemaphore.release()
    a1DoneSemaphore.acquire()
    statement2()

#### Monitor Implementation ####
lock = Lock()
a1DoneCondition = Condition(lock)
b1DoneCondition = Condition(lock)
a1Done = False
b1Done = False

def threadAm(statement1, statement2):
    global lock, a1DoneCondition, b1DoneCondtion, a1Done, b1Done
    statement1()
    with lock:
	a1Done = True
	a1DoneCondition.notify()
	while not b1Done:
	    b1DoneCondition.wait()
	statement2()

def threadBm(statement1, statement2):
    global lock, a1DoneCondition, b1DoneCondtion, a1Done, b1Done
    statement1()
    with lock:
	b1Done = True
	b1DoneCondition.notify()
	while not a1Done:
	    a1DoneCondition.wait()
	statement2()
	
#### Test Code ####
characterSelectedA = False
characterSelectedB = False

if __name__ == "__main__":
    def selectCharacterA():
	global characterSelectedA
	time.sleep(0.1)
	characterSelectedA = True

    def selectCharacterB():
	global characterSelectedB
	time.sleep(0.2)
	characterSelectedB = True

    def startGame():
	global characterSelectedA, characterSelectedB
	assert characterSelectedA and characterSelectedB
	# start game

    Thread(target = threadAs, args = (selectCharacterA, startGame)).start()
    Thread(target = threadBs, args = (selectCharacterB, startGame)).start()
    
    Thread(target = threadAm, args = (selectCharacterA, startGame)).start()
    Thread(target = threadBm, args = (selectCharacterB, startGame)).start()

    print('3.2 Rendezvous - Passed')    


    


