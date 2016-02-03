#!/usr/bin/python3
import os, fnmatch
files = []
for f in os.listdir("."):
    if fnmatch.fnmatch(f, "*[!README].md"):
        files.append(f)
tmp = ""
for fname in files:
    f = open(fname, "r")
    tmp += "\n---\n# " + fname + "\n"
    tmp += f.read()
    f.close()

wrt = open("README.md", "w")
wrt.write(tmp)
wrt.close()
