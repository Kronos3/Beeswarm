from read_csv import Clone, Set, RawIndexMapping, DictSet
import csv
from image_counter import ImageCounter
import matplotlib.pyplot as plt
from plot_grid import PlotGrid
from barchart import Barchart
from scipy import stats
import readline
import traceback
import sys
import re


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


def handle_location(unparsed: str):
	# typos
	typos = {
		"intescale": "interscale",
		"intersscale": "interscale",
		"Sacle": "scale"
	}
	for typo in typos:
		unparsed = unparsed.replace(typo, typos[typo])
	
	split = [y.strip() for y in re.split(",? ?", unparsed.lower().strip(" -?"))]
	return '-'.join(split)


split_location = split_data.split_col(
	RawIndexMapping.LOCATION,
	["scale", "interscale-line", "interscale-non-line"],
	"interscale", handle_location)
split_location = split_location.split_cols([RawIndexMapping.NBASAL, RawIndexMapping.NSUPRA], ["basal", "supra"], 0)


def apply_function(data, population, location, zlocation, __function):
	__daylist = (3.5, 7.0, 14.0, 30.0, 60.0, 90.0, 180.0, 365.0)
	if location == "total":
		return [__function(data.get_col(RawIndexMapping.NTOTAL, population, day)) for day in __daylist]
	else:
		return [__function(data.get(population, day, location, zlocation)) for day in __daylist]


def colpimg(data, counter, __max, population, location, zlocation):
	dl = (3.5, 7.0, 14.0, 30.0, 60.0, 90.0, 180.0, 365.0)
	normals = [__max / len(counter.out["%s,%s" % (population, day)]) for day in dl]
	if location == "total":
		return [len(data.get_col(RawIndexMapping.NTOTAL, population, dl[i])) * normals[i] for i in range(len(dl))]
	return [len(data.get(population, dl[i], location, zlocation)) * normals[i] for i in range(len(dl))]


def gen_beeswarms():
	iter_template = (("scale", "interscale-line", "interscale-non-line"), ("basal", "supra"), ("Dlx1", "Slc1a3"))
	main_figure = PlotGrid(split_location, image_counter, plt, iter_template)
	main_figure.save()


key_labels = (
				'Interscale line, Basal',
				'Interscale non-line, Basal',
				'Scale, Basal',
				'Interscale line, Supra-basal',
				'Interscale non-line, Supra-basal',
				'Scale, Supra-basal',
				"Total"
			)
colors = (
				"#1B2F33",
				"#28502E",
				"#47682C",
				"#8C7051",
				"#EF3054",
				"#70A0AF",
				"#706993",
				"#331E38",
			)


def gen_gmean():
	barfig = plt.figure(figsize=(8, 11))
	daylist = (3.5, 7.0, 14.0, 30.0, 60.0, 90.0, 180.0, 365.0)
	for i, pop in enumerate(("Dlx1", "Slc1a3")):
		Barchart(
			barfig.add_subplot(2, 1, i + 1),
			7,
			colors,
			key_labels,
			daylist,
			"Geometric Mean colony size for %s" % pop,
			"Day",
			"Geometric Mean colony size"
		).render_data((
			apply_function(split_location, pop, "interscale-line", "basal", stats.tstd),
			apply_function(split_location, pop, "interscale-non-line", "basal", stats.tstd),
			apply_function(split_location, pop, "scale", "basal", stats.tstd),
			apply_function(split_location, pop, "interscale-line", "supra", stats.tstd),
			apply_function(split_location, pop, "interscale-non-line", "supra", stats.tstd),
			apply_function(split_location, pop, "scale", "supra", stats.tstd),
			apply_function(split_data, pop, "total", "", stats.tstd)
		))
	barfig.savefig("gmean.png")


def gen_colpimg():
	barfig = plt.figure(figsize=(8, 11))
	daylist = (3.5, 7.0, 14.0, 30.0, 60.0, 90.0, 180.0, 365.0)
	for i, pop in enumerate(("Dlx1", "Slc1a3")):
		__max = image_counter.get_max()[0]
		graph_data = (
			colpimg(split_location, image_counter, __max, pop, "interscale-line", "basal"),
			colpimg(split_location, image_counter, __max, pop, "interscale-non-line", "basal"),
			colpimg(split_location, image_counter, __max, pop, "scale", "basal"),
			colpimg(split_location, image_counter, __max, pop, "interscale-line", "supra"),
			colpimg(split_location, image_counter, __max, pop, "interscale-non-line", "supra"),
			colpimg(split_location, image_counter, __max, pop, "scale", "supra"),
			colpimg(split_data, image_counter, __max, pop, "total", "")
		)
		Barchart(
			barfig.add_subplot(2, 1, i + 1),
			7,
			colors,
			key_labels,
			daylist,
			"Colonies per image %s" % pop,
			"Day",
			"Colonies per image"
		).render_data(graph_data)
	barfig.savefig("colpimg.png")


def gen_stddev():
	barfig = plt.figure(figsize=(8, 11))
	daylist = (3.5, 7.0, 14.0, 30.0, 60.0, 90.0, 180.0, 365.0)
	for i, pop in enumerate(("Dlx1", "Slc1a3")):
		Barchart(
			barfig.add_subplot(2, 1, i + 1),
			7,
			colors,
			key_labels,
			daylist,
			"Standard Deviation of colony sizes %s" % pop,
			"Day",
			"Standard Deviation"
		).render_data((
			apply_function(split_location, pop, "interscale-line", "basal", stats.tstd),
			apply_function(split_location, pop, "interscale-non-line", "basal", stats.tstd),
			apply_function(split_location, pop, "scale", "basal", stats.tstd),
			apply_function(split_location, pop, "interscale-line", "supra", stats.tstd),
			apply_function(split_location, pop, "interscale-non-line", "supra", stats.tstd),
			apply_function(split_location, pop, "scale", "supra", stats.tstd),
			apply_function(split_data, pop, "total", "", stats.tstd)
		))
	barfig.savefig("stddev.png")


def write_day(f, __list, delim):
	if not len(__list):
		f.write("0")
	else:
		f.write(delim.join(str(y) for y in __list))
	f.write("\n")


def export():
	dl = (3.5, 7.0, 14.0, 30.0, 60.0, 90.0, 180.0, 365.0)
	f = open("export.csv", "w+")
	
	delim = " "
	
	# Export image counts
	for population in ("Dlx1", "Slc1a3"):
		for day in dl:
			f.write(str(len(image_counter.out["%s,%s" % (population, day)])))
			if day != dl[-1]:
				f.write(delim)
		f.write("\n")
	# Export data
	for population in ("Dlx1", "Slc1a3"):
		for location in (
				('scale', 'basal'),
				('scale', 'supra'),
				('interscale-line', 'basal'),
				('interscale-line', 'supra'),
				('interscale-non-line', 'basal'),
				('interscale-non-line', 'supra'),
				"total"
		):
				for day in dl:
					if location == "total":
						write_day(f, split_data.get_col(RawIndexMapping.NTOTAL, population, day), delim)
					else:
						write_day(f, split_location.get(population, day, location[0], location[1]), delim)
	f.close()


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
		"export": export,
		"all": gen_all,
	}
	
	for arg in args[1:]:
		function_mappings[arg]()
		
	while True:
		try:
			exec("print(%s)" % input("> "))
		except KeyboardInterrupt:
			print("^C")
		except EOFError:
			print("^D")
			break
		except Exception:
			print(traceback.format_exc())


main(sys.argv)
