import zipfile as z
import re
from random import randint

name_r = re.compile(" \w+?_")
id_r = re.compile("_\d+_")

first = []
last = []
email = []
moodle = []

for name in z.ZipFile("./test_graid/day.zip").namelist():
    n = name[:name.find("_")].split(" ")
    first.append(n[0])
    last.append(n[1])
    moodle.append(re.findall(id_r, name)[0].replace("_", ""))

for l in last:
    q = l[:5].lower().replace("_", "x").replace(" ", "x").lower().ljust(5, "x") + format(randint(1, 999), "03d") + "@umn.edu"
    email.append(q)

n = zip(first, last, email, moodle)
with open("day_map.csv", "w") as fout:
    for i in n:
        fout.write(",".join(i) + "\n")
