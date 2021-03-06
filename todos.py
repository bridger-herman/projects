#!/usr/bin/env python3

import sys
from finder import search_dir

def display(line, number, filepath):
    print('{:03}  {}\n    {}'.format(number, filepath, line))

def main():
    search_term = 'TODO'
    if len(sys.argv) == 1:
        infos = search_dir(search_term, '.', print_incremental=False)
    elif len(sys.argv) == 2:
        infos = search_dir(search_term, sys.argv[1], print_incremental=False)
    else:
        print('bad argument')
        return
    for line, number, filepath in infos:
        display(line, number, filepath)

if __name__ == '__main__':
    main()
