#!/usr/bin/python3
import os, fnmatch, sys

try:
    d = sys.argv[1]
except IndexError:
    d = "."

files = []
for f in sorted(os.listdir(d)):
    if fnmatch.fnmatch(f, "*[!README].md"):
        files.append(f)
tmp = ""
for fname in files:
    f = open(fname, "r")
    tmp += "\n---\n` " + fname + "`\n---\n"
    tmp += f.read()
    f.close()

wrt = open("README.md", "w")
wrt.write(tmp)
wrt.close()
