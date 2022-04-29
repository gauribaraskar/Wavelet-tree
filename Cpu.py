import time

class CPU():

	# Measure time usage
	def __init__(self):
		self.start_time = None
		self.end_time = None

	def time_elapsed(self):
		return self.end_time - self.start_time

	def start_time(self):
		self.start_time = time.time()

	def end_time(self):
		self.end_time = time.time()

	# Add memory usage here