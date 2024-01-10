from threading import Thread, Lock, Condition, Semaphore
import time

"""
Signaling is the problem of allowing a thread to proceed only after another thread has signaled
that the thread may proceed. Note that there is NO order in who gets to go once the signal is
made.

An example might be a swarm of birds waiting to get into a bird house. Once a bird leaves the
bird house, another of the horde (any particular one) may get in."""

class SignalSemaphore:
    def __init__(self):
	self.signalSemaphore = Semaphore(0)

    def signal(self):
	self.signalSemaphore.release()

    def wait(self):
	self.signalSemaphore.acquire()

class SignalMonitor
    def __init__(self, n):
	self.lock = Lock()
	numSignals = 0
	signalsAvailableC = Condition(self.lock)

    def wait(self):
	with self.lock:
	    while self.numSignals == 0:
		self.signalsAvailableC.wait()

    def signal(self):
	with self.lock:
	    self.numSignals += 1
	    self.signalsAvailableC.notify()
	    
	

