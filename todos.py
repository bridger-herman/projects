#!/usr/bin/env python3

from finder import search_dir

def display(line, number, filepath):
    print('{:03}  {}\n    {}'.format(number, filepath, line))

def main():
    infos = search_dir('TODO')
    for line, number, filepath in infos:
        display(line, number, filepath)

if __name__ == '__main__':
    main()
