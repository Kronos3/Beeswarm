from beeswarm import *
from read_csv import Clone, Set, RawIndexMapping, DictSet
import csv

raw_data = []
for x in csv.reader(open("data.csv", "r")):
	temp = Clone(x, "sifisiiiis", [RawIndexMapping.NTOTAL, 0])
	if temp.add():
		raw_data.append(temp)

raw_data = Set(raw_data)

split_data = DictSet(raw_data.split_level([
	RawIndexMapping.POPULATION, RawIndexMapping.DAY,
	RawIndexMapping.MOUSE, RawIndexMapping.IMAGE
]))

split_location = split_data.split_cols([RawIndexMapping.NBASAL, RawIndexMapping.NSUPRA], ["basal", "supra"])

#print(split_location)
print (split_location.get ("Dlx1", 3.5,
                           1, 1,
                           "basal"))

#beeswarm([d1], method="swarm", l)
#beeswarm([d1], method="center")
