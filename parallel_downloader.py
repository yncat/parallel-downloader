# -*- coding: utf-8 -*-
import math
import threading
import time
import urllib.request

class _listWorker(threading.Thread):
	def __init__(self,parent,downloads):
		threading.Thread.__init__(self)
		self.parent=parent
		self.downloads=downloads

	def run(self):
		for elem in self.downloads:
			try:
				urllib.request.urlretrieve(elem[0],elem[1])
			except Exception as e:
				self.parent._pushError(elem,str(e))
				continue
			#end exception
			self.parent._pushSuccess()
		#end for
	#end run

class ParallelDownloader(object):
	def __init__(self,number_of_worker_threads=4):
		self.number_of_worker_threads=number_of_worker_threads
		self.downloads=[]
		self.succeeded_num=0
		self.processed_num=0
		self.failures_list=[]

	def append(self,url,save_filename):
		self.downloads.append((url,save_filename))

	def start(self):
		started=time.time()
		n=math.ceil(len(self.downloads)/self.number_of_worker_threads)
		devide=[self.downloads[idx:idx+n] for idx in range(0,len(self.downloads),n)]
		if len(devide)<self.number_of_worker_threads:
			print("Decreasing number of worker threads to %d (originally %d" % (len(devide),self.number_of_worker_threads))
			self.number_of_worker_threads=len(devide)
		#end thread decreasing
		threads=[]
		for i in range(self.number_of_worker_threads):
			threads.append(_listWorker(self,devide[i]))
		#end make threads
		for thread in threads:
			thread.start()
		#end start thread
		counter=0
		while(True):
			counter+=1
			if counter==10:
				counter=0
				print("\r%d%%" % (self.processed_num/len(self.downloads)*100), end="")
			#end display percent
			if self.processed_num==len(self.downloads): break
			time.sleep(0.1)
		#end display progress
		for thread in threads:
			thread.join()
		#end join thread
		elapsed=time.time()-started
		print("")
		print("Downloaded %d/%d files in %.2f seconds." % (self.succeeded_num,self.processed_num,elapsed))
		if len(self.failures_list)>0:
			print("Failed files:")
			for elem in self.failures_list: print("%s: %s (%s)" % (elem[1],elem[2],elem[0]))
		#end error

	def _pushSuccess(self):
		self.processed_num+=1
		self.succeeded_num+=1

	def _pushError(self,elem,error):
		self.failures_list.append((elem[0],elem[1],error))
		self.processed_num+=1
