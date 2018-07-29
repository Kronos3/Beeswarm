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
	day_order = (3.5, 7.0, 14.0, 30.0, 60.0, 90.0, 180.0, 365.0)
	
	"""
	:argument parent PlotGrid parent
	:argument sel 2 Tuple (POPULATION, LOCATION)
	"""
	def __init__(self, parent, figure, sel, plot_t, cap):
		self.parent = parent
		self.cap = cap
		self.normalize = []
		self.data = []
		self.x_labels = []
		self.selector = sel
		
		for day in Plot.day_order:
			c_normal = parent.image_n / len(parent.image_counter.out["%s,%s" % (sel[0], day)])
			self.normalize.append(c_normal)
			current_data = normalize_data(self.parent.data.get(sel[0], day, sel[1]), c_normal)
			gm = round(float(stats.gmean(current_data)), 3)
			cpi = len(current_data) * c_normal
			sd = round(float(stats.tstd(current_data)), 3)
			text = "%s\nx̅: %s\nCol/img: %s\nσ: %s" % (
				day, gm, cpi, sd)
			self.x_labels.append(text)
			self.data.append(Plot.cap(current_data, self.cap))
		
		self.figure = figure
		self.plot_tuple = plot_t
		self.graph_label = "%s population, %s" % (sel[0], sel[1].replace("supra", "supra-basal"))
	
	@staticmethod
	def cap(data, cap):
		for i in range(len(data)):
			if data[i] > cap:
				data[i] = cap
		return data
	
	def plot(self):
		if self.selector[0] == "Slc1a3" and self.selector[1] == "supra":
			for i, day in enumerate(self.data):
				if 0 in day:
					print(day)
					print(Plot.day_order[i])
		
		bs, ax = beeswarm(
			self.data,
			method="center",
			s=.5,
			__s=10,
			labelrotation="horizontal",
			ax=self.figure.add_subplot(*self.plot_tuple), labels=self.x_labels,
			col="white",
			edgecolors="black"
		)
		if self.plot_tuple[2] != 1:
			ax.set_xlabel("Day & frequency")
		ax.set_ylabel("Colony Size (cells)")
		ax.set_title(self.graph_label)
		ax.set_ylim(bottom=0, top=self.cap)
		ax.set_yticks((0, 10, 20, 30, 40))
		ax.grid(color='black', linestyle='-', linewidth=.5, axis="y")


class PlotGrid:
	def __init__(self, data, counter, plot, iter_template, cap=40):
		self.data = data
		self.image_counter = counter
		self.figures = []
		self.image_n = counter.get_max()[0]
		self.plots = []
		self.cap = cap
		
		self.dimensions = [2, 1]
		self.figure_dimensions = (11, 8)
		
		for location in iter_template[0]:
			current_fig = plot.figure(figsize=self.figure_dimensions)
			current_fig.set_tight_layout({"pad": .0})
			i = 1
			for population in iter_template[1]:
				temp = Plot(self, current_fig, (population, location), (*self.dimensions, i), self.cap)
				temp.plot()
				self.plots.append(temp)
				i += 1
			current_fig.tight_layout()
			current_fig.subplots_adjust(top=.6, bottom=.5)
			self.figures.append(current_fig)
	
	def save(self, names):
		for i, fig in enumerate(self.figures):
			fig.savefig(names[i])
