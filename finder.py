#!/usr/bin/python3
# Recurisve finder for text files

import re
from os import walk, path
from sys import argv

def display(line, number, filepath):
    print('line {:03}, {}'.format(number, filepath))

def search_file(filepath, key = "", regex = False, ignore_case = True):
    fin = open(filepath, "r")
    key = key.lower() if ignore_case else key
    i = 1
    infos = []
    try:
        for line in fin:
            match = False
            line = line.lower() if ignore_case else line
            if regex:
                match = bool(re.search(key, line))
            else:
                match = key in line
            if match:
                infos.append((line, i, filepath))
            i += 1
    except UnicodeDecodeError:
        pass
    fin.close()
    return infos


def search_dir(term, directory='.', regex=False, ignore_case=True):
    w = walk(directory)
    infos = []
    for (top, dirs, files) in w:
        for f in files:
            infos += search_file(path.join(top, f), term, regex,
                    ignore_case)
    return infos

def main():
    options = {"i": "ignore case", "r": "use regular expression"}
    try:
        flags = re.findall(r" -\w+", "".join(argv[1:]))
        flags = [flag[2:] for flag in flags]
        flags = list("".join(flags))
        for flag in flags:
            if flag not in options:
                raise IndexError
        infos = search_dir(argv[1], '.', 'r' in flags, 'i' in flags)
        for line, number, filepath in infos:
            display(line, number, filepath)
        print(argv[1], "occurred on", len(infos), "lines")
    except IndexError:
        print("Usage: ./finder.py key <options>")
        print("Options:")
        [print(" "*3, option, ":", options[option]) for option in options]

if __name__ == '__main__':
    main()
