from fnmatch import fnmatch
from os import listdir
import re

name_r = re.compile(" \w+?_")
id_r = re.compile("_\d+_")

ofile = open("day.csv", "w")

for f in listdir("day"):
    if fnmatch(f, "*.py"):
        ofile.write(re.findall(id_r, f)[0][1:-1] + "," + re.findall(name_r, f)[0][1:6].replace("_", "x").replace(" ", "x").lower().ljust(5, "x") + "001" + "\n")
        # print(re.findall(name_r, f)[0][1:6].replace("_", "x").replace(" ", "x").lower().ljust(5, "x") + "001", end = "\t")
        # print(re.findall(id_r, f)[0][1:-1])
ofile.close()
