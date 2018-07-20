from read_csv import Clone, Set, RawIndexMapping, DictSet
import csv
from image_counter import ImageCounter
import matplotlib.pyplot as plt
from plot_grid import PlotGrid


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
iter_template = (("basal", "supra"), ("Dlx1", "Slc1a3"))
main_figure = PlotGrid(split_location, image_counter, plt, iter_template)
# main_figure.show()
main_figure.save(("basal.png", "supra.png"))
