import cv2
import threading
import time

class VideoCapture():
	def __init__(self, url, timeout=0.05):
		self.url = url
		self.t = threading.Thread(target=self.thread)
		self.stop_thread = False
		self.timeout = timeout
	
	def thread(self):
		while True:
			if self.stop_thread == True:
				return
			self.ret, self.frame = self.cap.read()
			time.sleep(self.timeout)

	def init(self):
		self.cap = cv2.VideoCapture(self.url)
		self.ret, self.frame = self.cap.read()
		self.t.start()
		print('Started asyncronous fetch')
		return self.ret, self.frame
	
	def read(self):
		return self.ret, self.frame
	
	def release(self):
		self.stop_thread = True
		time.sleep(1)