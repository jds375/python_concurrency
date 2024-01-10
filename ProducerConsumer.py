from threading import Thread, Lock, Condition, Semaphore
import time
"""
Producer-Consumer is the problem of having m producer threads produce items
that are then consumed by n consumer threads. A consumer thread can only
proceed if there is an available item for it to consume.

An example is a batch math computation engine. The producer threads collect a set of 
data and package it. It is then passed off to a consumer that computes something
using the data.
"""

class ProducerConsumerSemaphore:
    def __init__(self, n):
	self.n = n
	self.buff = []
	self.mutex = Semaphore(1)
	self.itemsSema = Semaphore(0)
	self.spacesSema = Semaphore(n)

    def produce(self, p):
	item = p()
	self.spaces.acquire()
	self.mutex.acquire()
	self.buffer.append(item)
	self.mutex.release()
	self.items.release()

    def consume(self, c):
	self.items.acquire()
	self.mutex.acquire()
	item = self.buff.pop(0)
	self.mutex.release()
	self.spaces.release()
	c(item)

class ProducerConsumerMonitor:
    def __init__(self, n):
	self.n = n
	self.buff = []
	self.lock = Lock()
	self.itemAvailable = Condition(self.lock)
	self.roomInBuffer = Condition(self.lock)

    def producer(self, p):
	item = p()
	with self.lock:
	    while len(self.buff) == self.n:
		self.roomInBuffer.wait()
	    self.buff.append(item)
	    self.itemAvailable.notify()

    def consumer(self, c):
	item = None
	with self.lock:
	    while len(self.buff) == 0:
		self.itemAvailable.wait()
	    item = self.buff.pop(0)
	    self.roomInBuffer.notify()
	c(item)
	    
