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
	def __init__ (self, data=None):
		if data is None:
			data = {}
		self.data = data
	
	def split_col(self, index, selectors, default, apply_function):
		out = {}
		for key in self.data:
			for clone in self.data[key]:
				new_key = eval(key)
				parsed = apply_function(clone.data[index])
				if parsed not in selectors:
					print("location %s for key %s not found (%s)" % (parsed, key, clone.data[index]))
					parsed = default
				
				new_key.append (parsed)
				new_key = str(new_key)
				
				try:
					out[new_key]
				except KeyError:
					out[new_key] = []
				out[new_key].append(clone)
		
		return DictSet(out)
	
	def split_cols(self, indecies, selectors, skip):
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
					if clone.data[indecies[i]] != skip:
						out[new_key].append (clone.data[indecies[i]])
		
		return DictSet(out)
	
	def get_col(self, index, *args):
		return [x[index] for x in self.get(*args)]
	
	def get (self, *args):
		key = str(list(args))
		try:
			self.data[key]
		except KeyError:
			self.data[key] = []
		return self.data[key]
	
	def __str__ (self):
		return str(self.data)

cdef class Set:
	def __init__(self, data=None):
		if data is None:
			data = []
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
	
	def __getitem__ (self, index: int):
		return self.data[index]
	
	def add (self):
		return self.to_add

