from scipy import stats
from beeswarm import *


def normalize_data(data, normalization_factor):
	unique = {}
	for x in data:
		try:
			unique[x]
		except KeyError:
			unique[x] = 0
		unique[x] += 1
	
	out = []
	for item in unique:
		for i in range(int(unique[item] * normalization_factor)):
			out.append(item)
	
	return out


class Plot:
	def __init__(self, parent, sel, plot_t):
		self.parent = parent
		self.normalize = parent.image_n / len(parent.image_counter.out["%s,%s" % (sel[0], sel[1])])
		self.data = normalize_data(self.parent.data.get(sel[0], sel[1], sel[2]), self.normalize)
		self.figure = parent.figure
		self.plot_tuple = plot_t
		
		self.no_zero = [x for x in self.data if x != 0]
		
		self.geometric_mean = round(float(stats.gmean(self.no_zero)), 3)
		# self.geometric_mean = stats.gmean(self.data)
		# print (self.data)
		self.col_per_image = len(self.no_zero) * self.normalize
		self.standard_deviation = round(float(stats.tstd(self.data)), 3)
		self.graph_label = "%s @ %s, %s" % (sel[0], sel[1], sel[2].replace("supra", "supra-basal"))
		self.text_index = 0
	
	def plot(self):
		text = """gmean col size: %s\nCol/img: %s\nμ: %s""" % (self.geometric_mean, self.col_per_image, self.standard_deviation)
		
		bs, ax = beeswarm(self.data, method="center", s=3, ax=self.figure.add_subplot(*self.plot_tuple))
		ax.set_title(self.graph_label)
		ax.text(1, 1, text, horizontalalignment='right', verticalalignment='top', transform=ax.transAxes)


class PlotGrid:
	def __init__(self, data, counter, figure):
		self.data = data
		self.image_counter = counter
		self.figure = figure[0]
		self.image_n = counter.get_max()[0]
		self.plots = []
		
		self.dimensions = [8, 2]
		self.figure.set_tight_layout({"pad": .0})
		
		i = 1
		for key in list(self.data.data.keys())[:int(len(self.data.data.keys())/2)]:
			temp = Plot(self, eval(key), (*self.dimensions, i))
			temp.plot()
			self.plots.append(temp)
			
			i += 1
		
		self.figure = figure[1]
		self.figure.set_tight_layout({"pad": .0})
		i = 1
		for key in list(self.data.data.keys())[int(len(self.data.data.keys()) / 2):]:
			temp = Plot(self, eval(key), (*self.dimensions, i))
			temp.plot()
			self.plots.append(temp)
			
			i += 1
		
		self.figure = figure
	
	def show(self):
		for fig in self.figure:
			fig.show()