from threading import Thread, Lock, Condition, Semaphore
import time
"""
Reader-Writer is the problem of letting n reader threads enter shared state, but only letting
one writer thread enter/modify shared state at a given time. Note that to prevent starvation
this is a nontrivial problem. We should stop letting people read once a writer arrives.

The obvious example of this is reader and writing to a file.
"""
class ReaderWriterSemaphore:
    class Lightswitch:
	def __init__(self):
	    self.count = 0
	    self.mutex = Semaphore(1)
	
	def lock(self, semaphore):
	    self.mutex.acquire()
	    self.count += 1
	    if self.count == 1:
		semaphore.acquire()
	    self.mutex.release()

	def unlock(self, semaphore):
	    self.mutex.acquire()
	    self.count -= 1
	    if self.count == 0:
		semaphore.release()
	    self.mutex.release()

    def __init__(self):
	self.turnstile = Semaphore(1)
	self.lightswitch = Lightswitch()
	self.roomEmpty = Semaphore(1)

    def read(self, r):
	self.turnstile.acquire()
	self.turnstile.release()
	self.lightswitch.lock(self.roomEmpty)
	r()
	self.lightswtich.unlock(self.roomEmpty)

    def write(self, w):
	self.turnstile.acquire()
	self.roomEmpty.acquire()
	w()
	self.turnstile.release()
	self.roomEmpty.release()

class ReaderWriterMonitor:
    def __init__(self):
	self.numR = 0
	self.numW = 0
	self.writing = False
	self.lock = Lock()
	self.doneWriting = Condition(self.lock)
	self.doneReading = Condition(self.lock)

    def read(self, r):
	with self.lock:
	    while self.numW > 0:
		self.doneWriting.wait()
	    self.numR += 1
	r()
	with self.lock:
	    self.numR -= 1
	    if self.numR == 0:
		self.doneReading.notify()

    def write(self, r):
	with self.lock:
	    self.numW += 1
	    while self.numR > 0 or self.writing:
		if self.numR > 0:
		    self.doneReading.wait()
		if self.writing:
		    self.doneWriting.wait()
	    self.writing = True
	w()
	with self.lock:
	    self.numW -= 1
	    self.writing = False
	    self.doneWriting.notifyAll()
