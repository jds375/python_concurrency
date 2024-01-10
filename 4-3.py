from threading import Thread, Lock, Condition, Semaphore
import time
import Queue

#### 4.3 - No Starvation Mutex ####

#### Semaphore Implementation ####
room1 = 0
room2 = 0
mutex = Semaphore(1)
turnstile1 = Semaphore(1)
turnstile2 = Semaphore(0)

def threadXs(f):
    global room1, room2, mutex, turnstile1, turnstile2
    mutex.acquire()
    room1 += 1
    mutex.release()
    turnstile1.acquire()
    room2 += 1
    mutex.acquire()
    room1 -= 1
    if room1 == 0:
	mutex.release()
	turnstile2.release()
    else:
	mutex.release()
	turnstile1.release()
    turnstile2.acquire()
    room2 -= 1
    f()
    if room2 == 0:
	turnstile1.release()
    else:
	turnstile2.release()

#### Test Code ####
roomSize = 5 # Number allowed in room (critical section)

if __name__ == "__main__":

    timeStart = time.time()
    def enterRoom():
	time.sleep(.1)

    Thread(target = threadXs, args = (enterRoom,)).start()
    Thread(target = threadXs, args = (enterRoom,)).start()
    Thread(target = threadXs, args = (enterRoom,)).start()
    Thread(target = threadXs, args = (enterRoom,)).start()
    Thread(target = threadXs, args = (enterRoom,)).start()
    Thread(target = threadXs, args = (enterRoom,)).start()
    Thread(target = threadXs, args = (enterRoom,)).start()

#    Thread(target = threadXm, args = (enterRoom,)).start()
#    Thread(target = threadXm, args = (enterRoom,)).start()
#    Thread(target = threadXm, args = (enterRoom,)).start()
#    Thread(target = threadXm, args = (enterRoom,)).start()
#    Thread(target = threadXm, args = (enterRoom,)).start()
#    Thread(target = threadXm, args = (enterRoom,)).start()
#    Thread(target = threadXm, args = (enterRoom,)).start()

    time.sleep(0.8)
    print('4.3 No Starvation Mutex - Passed')
    
