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

cdef class DictSet:
	def __init__ (self, data={}):
		self.data = data
	
	def split_cols(self, indecies, selectors):
		out = {}
		
		for key in self.data:
			for i in range (len (indecies)):
				evaled = eval(key)
				evaled.append (selectors[i])
				new_key = str(evaled)
				try:
					out[new_key]
				except KeyError:
					out[new_key] = []
				for clone in self.data[key]:
					out[new_key].append (clone.data[indecies[i]])
		
		return DictSet(out)
	
	def get (self, *args):
		return self.data[str(list(args))]
	
	def __str__ (self):
		return str(self.data)

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
		out = {}
		
		hash_clone = lambda row,props: str([row[x] for x in props])
		
		for clone in self.data:
			__hash = hash_clone(clone.data, prop_list)
			try:
				out[__hash]
			except KeyError:
				out[__hash] = []
			out[__hash].append (clone)
		
		return out


cdef class Clone:
	def __init__ (self, csv_line, template, ignore_set):
		self.data = []
		self.to_add = True
		for i, x in enumerate(csv_line):
			if template[i] == 's':
				self.data.append (x)
			else:
				if len (x) == 0:
					x = 0
				parsed = x
				if template[i] == 'i':
					parsed = int (parsed)
				elif template[i] == 'f':
					parsed = float (parsed)
				if i == ignore_set[0] and parsed == ignore_set[1]:
					self.to_add = False
					break
				self.data.append (parsed)
	
	def add (self):
		return self.to_add

