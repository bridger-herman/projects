#!/usr/bin/env python3
# Recurisve finder for text files

import re
import argparse
from os import walk, path
from fnmatch import fnmatch

DEFAULT_IGNORE_PATTERNS = ['.git/*', '.gitignore', '*.swp', '__pycache__/*',
        'target/*']

def display(line, number, filepath):
    print('{: 5}, {}'.format(number, filepath))

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

def matches_exclude(exclude_patterns, pattern):
    if pattern.startswith('./'):
        pattern = pattern[2:]
    return any([fnmatch(pattern, p) for p in exclude_patterns])

def search_dir(term, directory, exclude_patterns=None, regex=False,
        ignore_case=True, print_incremental=True):
    w = walk(directory)
    infos = []
    for (top, dirs, files) in w:
        if matches_exclude(exclude_patterns, top):
            continue
        for f in files:
            if matches_exclude(exclude_patterns, f):
                continue
            new_infos = search_file(path.join(top, f), term, regex, ignore_case)
            if print_incremental:
                for info in new_infos:
                    display(*info)
            infos += new_infos
    return infos

def main():
    options = {"i": "ignore case", "r": "use regular expression"}
    parser = argparse.ArgumentParser()
    parser.add_argument('term', help='search term')
    parser.add_argument('-i', '--ignore', help='ignore case', \
            action='store_true')
    parser.add_argument('-r', '--regex', help='use regular expression',
            action='store_true')
    parser.add_argument('-c', '--print-incremental', \
            help='print search results incrementally', action='store_true')
    parser.add_argument('-s', '--search-dir', help='directory to search')
    parser.add_argument('-x', '--exclude', help='exclude file patterns (comma-separated)')
    args = parser.parse_args()

    exclude_patterns = DEFAULT_IGNORE_PATTERNS if args.exclude is None \
            else DEFAULT_IGNORE_PATTERNS + args.exclude.split(',')

    try:
        infos = search_dir(args.term, \
                '.' if args.search_dir is None else args.search_dir, \
                exclude_patterns, args.regex, args.ignore,
                args.print_incremental
        )
        if not args.print_incremental:
            for line, number, filepath in infos:
                display(line, number, filepath)
        print(args.term, "occurred on", len(infos), "lines")
    except IndexError:
        print("Usage: ./finder.py key <options>")
        print("Options:")
        [print(" "*3, option, ":", options[option]) for option in options]

if __name__ == '__main__':
    main()
