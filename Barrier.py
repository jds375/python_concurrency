from threading import Thread, Lock, Condition, Semaphore
import time

"""
Barrier is the problem of only letting n threads proceed after all n have done something first.
Here, we consider a reusable barrier. That is, the barrier should be able to be used multiple
times, which complicates the code a bit from a non-reusable one.

An example of such might be starting a multi-player videogame. All n players must call
playerReady() before the function playGame() is allowed to proceed for each thread.
"""

class BarrierSemaphore:
    def __init__(self, n):
	self.n = n
	self.numInBarrier = 0
	self.mutex = Semaphore(1)
	self.turnstile1Sema = Semaphore(0)
	self.turnstile2Sema = Semaphore(1)

    def enterBarrier(self):
	self.mutex.acquire()
	self.numInBarrier += 1
	if self.numInBarrier == self.n:
	    self.turnstile2Sema.acquire()
	    self.turnstile1Sema.release()
	self.mutex.release()
	self.turnstile1Sema.acquire()
	self.turnstile1Sema.release()
	self.mutex.acquire()
	self.numInBarrier -= 1
	if self.numInBarrier == 0:
	    self.turnstile1Sema.acquire()
	    self.turnstile2Sema.release()
	self.mutex.release()
	self.turnstile2Sema.acquire()
	self.turnstile2Sema.release()

class BarrierMonitor:
    def __init__(self, n):
	self.n = n
	self.numTurnstile1 = 0
	self.numTurnstile2 = 0
	self.lock = Lock()
	self.turnstile1FullC = Condition(self.lock)
	self.turnstile2FullC = Condition(self.lock)

    def enterBarrier(self):
	with self.lock:
	    self.numTurnstile1 += 1
	    if self.numTurnstile1 == self.n:
		self.numTurnstile2 = 0
		self.turnstile1FullC.notifyAll()
	    else:
		while self.numTurnstile1 != self.n:
		    self.turnstile1FullC.wait()
	with self.lock:
	    self.numTurnstile2 += 1
	    if self.numTurnstile2 == self.n:
		self.numTurnstile1 = 0
		self.turnstile2FullC.notifyAll()
	    else:
		while self.numTurnstile2 != self.n
		    self.turnstile2FullC.wait()
