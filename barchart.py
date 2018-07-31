import numpy as np


class Barchart:
	def __init__(self, ax, bar_n, color_seq, key_labels, labels, title="", xlabel="", ylabel=""):
		self.bar_n = bar_n
		self.color_seq = color_seq
		
		self.labels = labels
		self.key_labels = key_labels
		self.title = title
		self.xlabel = xlabel
		self.ylabel = ylabel
		
		self.ax = ax
		self.g_index = np.array([np.log2(x) for x in self.labels])
		self.bar_width = 0.07
	
	def reset_axis(self):
		self.ax.clear()
		
		self.ax.set_xticks(self.g_index + self.bar_width)
		self.ax.set_xticklabels(self.labels)
		self.ax.set_title(self.title)
		self.ax.set_xlabel(self.xlabel)
		self.ax.set_ylabel(self.ylabel)
		self.ax.grid(color='black', linestyle='-', linewidth=.25, axis="y")
	
	def render_data(self, data):
		self.reset_axis()
		
		for i in range(self.bar_n):
			self.ax.bar(
				self.g_index + (((i + 2) - self.bar_n / 2) * self.bar_width),
				data[i],
				self.bar_width,
				alpha=1, color=self.color_seq[i],
				label=self.key_labels[i])
		self.ax.legend()
