from read_csv import Clone, Set, RawIndexMapping, DictSet
import csv
from image_counter import ImageCounter
import matplotlib.pyplot as plt
from plot_grid import PlotGrid
from barchart import Barchart
from scipy import stats
import sys


raw_data = []
for x in csv.reader(open("data.csv", "r")):
	temp = Clone(x, "sifisiiiis", (RawIndexMapping.NTOTAL, 0))
	if temp.add():
		raw_data.append(temp)

raw_data = Set(raw_data)
image_counter = ImageCounter(
	raw_data.data, RawIndexMapping.MOUSE,
	RawIndexMapping.IMAGE, RawIndexMapping.POPULATION, RawIndexMapping.DAY)
image_counter.process()

split_data = DictSet(raw_data.split_level([
	RawIndexMapping.POPULATION, RawIndexMapping.DAY
]))

split_location = split_data.split_cols([RawIndexMapping.NBASAL, RawIndexMapping.NSUPRA], ["basal", "supra"], 0)


def apply_function(data, population, location, __function):
	__daylist = (3.5, 7.0, 14.0, 30.0, 60.0, 90.0, 180.0, 365.0)
	if location == "total":
		return [__function(data.get_col(RawIndexMapping.NTOTAL, population, day)) for day in __daylist]
	else:
		return [__function(data.get(population, day, location)) for day in __daylist]


def colpimg(data, counter, __max, population, location):
	dl = (3.5, 7.0, 14.0, 30.0, 60.0, 90.0, 180.0, 365.0)
	normals = [__max / len(counter.out["%s,%s" % (population, day)]) for day in dl]
	if location == "total":
		return [len(data.get_col(RawIndexMapping.NTOTAL, population, dl[i])) * normals[i] for i in range(len(dl))]
	return [len(data.get(population, dl[i], location)) * normals[i] for i in range(len(dl))]


def gen_beeswarms():
	iter_template = (("basal", "supra"), ("Dlx1", "Slc1a3"))
	main_figure = PlotGrid(split_location, image_counter, plt, iter_template)
	main_figure.save(("basal.png", "supra.png"))


def gen_gmean():
	barfig = plt.figure(figsize=(8, 11))
	daylist = (3.5, 7.0, 14.0, 30.0, 60.0, 90.0, 180.0, 365.0)
	for i, pop in enumerate(("Dlx1", "Slc1a3")):
		Barchart(
			barfig.add_subplot(2, 1, i + 1),
			3,
			("green", "blue", "orange"),
			("Basal", "Supra", "Total"),
			daylist,
			"Geometric Mean colony size for %s" % pop,
			"Day",
			"Geometric Mean colony size"
		).render_data((
			apply_function(split_location, pop, "basal", stats.gmean),
			apply_function(split_location, pop, "supra", stats.gmean),
			apply_function(split_data, pop, "total", stats.gmean)
		))
	barfig.savefig("gmean.png")


def gen_colpimg():
	barfig = plt.figure(figsize=(8, 11))
	daylist = (3.5, 7.0, 14.0, 30.0, 60.0, 90.0, 180.0, 365.0)
	for i, pop in enumerate(("Dlx1", "Slc1a3")):
		__max = len(image_counter.get_max())
		Barchart(
			barfig.add_subplot(2, 1, i + 1),
			3,
			("green", "blue", "orange"),
			("Basal", "Supra", "Total"),
			daylist,
			"Colonies per image %s" % pop,
			"Day",
			"Colonies per image"
		).render_data((
			colpimg(split_location, image_counter, __max, pop, "basal"),
			colpimg(split_location, image_counter, __max, pop, "supra"),
			colpimg(split_data, image_counter, __max, pop, "total")
		))
	barfig.savefig("colpimg.png")


def gen_stddev():
	barfig = plt.figure(figsize=(8, 11))
	daylist = (3.5, 7.0, 14.0, 30.0, 60.0, 90.0, 180.0, 365.0)
	for i, pop in enumerate(("Dlx1", "Slc1a3")):
		__max = len(image_counter.get_max())
		Barchart(
			barfig.add_subplot(2, 1, i + 1),
			3,
			("green", "blue", "orange"),
			("Basal", "Supra", "Total"),
			daylist,
			"Standard Deviation of colony sizes %s" % pop,
			"Day",
			"Standard Deviation"
		).render_data((
			apply_function(split_location, pop, "basal", stats.tstd),
			apply_function(split_location, pop, "supra", stats.tstd),
			apply_function(split_data, pop, "total", stats.tstd)
		))
	barfig.savefig("stddev.png")


def main(args):
	def gen_all():
		for key in function_mappings:
			if key != "all":
				function_mappings[key]()
	
	function_mappings = {
		"beeswarm": gen_beeswarms,
		"gmean": gen_gmean,
		"colpimg": gen_colpimg,
		"stddev": gen_stddev,
		"all": gen_all,
	}
	
	for arg in args[1:]:
		function_mappings[arg]()


main(sys.argv)
