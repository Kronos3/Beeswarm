cpdef enum RawIndexMapping:
	POPULATION,
	MOUSE,
	DAY
	IMAGE,
	TILE,
	CLONE,
	NBASAL,
	NSUPRA,
	NTOTAL,
	LOCATION

cdef class Set:
	def __init__(self, data=[]):
		self.data = data
	
	def pop (self, prop, value):
		out = []
		
		i = 0
		while i < len (self.data):
			if self.data[i].prop == value:
				out.append (self.data.pop(i))
				i -= 1
			i += 1
	
		return out
	
	def append (self, item):
		self.data.append(item)
	
	def split (self, prop):
		out = {}
		for x in self.data:
			try:
				out[x.data[prop]]
			except KeyError:
				out[x.data[prop]] = Set ()
			out[x.data[prop]].append (x)
		
		return out
	
	def split_level (self, prop_list):
		print (prop_list)
		out = self.split(prop_list[0])
		
		if len (prop_list) <= 1:
			return out
		
		for t in out:
			out[t] = out[t].split_level(prop_list[1:])
		
		return out


cdef class Clone:
	def __init__ (self, csv_line, template):
		self.data = []
		for i, x in enumerate(csv_line):
			if template[i] == 's':
				self.data.append (x)
			else:
				if len (x) == 0:
					x = 0
				if template[i] == 'i':
					self.data.append (int (x))
				elif template[i] == 'f':
					self.data.append (float (x))

