cdef class Set:
	cpdef public data

cdef class Clone:
	cdef public data
	cdef readonly to_add

cdef class DictSet:
	cdef public data