from threading import Thread, Lock, Condition, Semaphore
import time

"""
Mutual Exclusion is the problem of providing m threads exclusive access to an instance of shared
state given a set of n threads where m<n.

An example of such is n users trying modify a single instance of company's bank data. We need to
allow only one user be modifying it at a time, so that the data doesn't get jumbled.

Another example where we allow m users instead of n would be a small playground. We can't let all
kids go on the playground, otherwise things will get messed up. Instead, we only let a small subset
at a given time.
"""

#### Semaphore Solution ####
class MutualExclusionSemaphore:
    def __init__(self, n):
	self.mutex = Semaphore(n)

    def function(self, f):
	self.mutex.acquire()
	self.f()
	self.mutex.release()

#### Monitor Solution ####
class MutualExclusionMonitor:
    def __init__(self, n):
	self.n = n
	self.lock = Lock()
	self.threadsInside = 0
	self.roomAvailable = Condition(self.lock)

    def function(self, f):
	with self.lock:
	    while self.threadsInside == self.n:
		self.roomAvailable.wait()
	    self.threadsInside += 1
	f()
	with self.lock:    
	    self.threadsInside -= 1
	    self.roomAvailable.notify()
