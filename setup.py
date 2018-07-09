from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

ex = [
	"read_csv"
]

extensions = []
for x in ex:
	extensions.append(Extension(
		'%s' % x, ["%s.pyx" % x],
	))

setup(
	ext_modules=cythonize(extensions)
)