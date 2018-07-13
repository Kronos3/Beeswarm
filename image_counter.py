class ImageCounter:
	def __init__(self, data, mouse_index, image_index, pop_index=-1, day_index=-1):
		self.mouse_index = mouse_index
		self.image_index = image_index
		self.pop_index = pop_index
		self.day_index = day_index
		self.data = data
		self.out = {}
	
	def process(self):
		self.out = {}
		i = 0
		for d in self.data:
			pop = ""
			day = ""
			if self.pop_index != -1:
				pop = d[self.pop_index]
			if self.day_index != -1:
				day = d[self.day_index]
			__hash = "%s,%s" % (pop, day)
			__item = "%d,%d" % (d[self.mouse_index], d[self.image_index])
			
			try:
				self.out[__hash]
			except KeyError:
				self.out[__hash] = []
			
			if __item not in self.out[__hash]:
				self.out[__hash].append(__item)
			i += 1
		
		return self.out
	
	def get_max(self):
		__max = -1
		__item = None
		for d in self.out:
			if len(self.out[d]) > __max:
				__max = len(self.out[d])
				__item = d
		
		return __max, __item, self.out[__item]
