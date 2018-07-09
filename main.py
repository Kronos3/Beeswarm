from beeswarm import *
from read_csv import Clone, Set, RawIndexMapping
import csv

raw_data = []
for x in csv.reader(open("data.csv", "r")):
	raw_data.append(Clone(x, "sifisiiiis"))

raw_data = Set(raw_data)

split_data = raw_data.split_level([RawIndexMapping.POPULATION, RawIndexMapping.DAY])

#beeswarm([d1], method="swarm")
#beeswarm([d1], method="center")
