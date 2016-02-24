#!/usr/bin/python3

import sys
import json
from os import path, chdir, system
from completer import ListCompleter

HOME = path.expanduser("~")
FILENAME = ".favorites"
# Operations:
# + Add a favorite
#  + With nicknames
#  + Store frequencies along with
# + List favorites
# + Remove a favorite
# Store in ~/.favorites

def read_file(fname):
    try:
        d = json.load(open(fname, "r"))
    except FileNotFoundError:
        print("favorites: unable to load file")
        return None
    return d

def add_fav(*args):
    try:
        if len(args) > 1:
            link = args[1]
            nick = args[0]
        else:
            link = args[0]
            nick = args[0]
        link = path.realpath(path.expanduser(link))
    except IndexError:
        print("favorites: nothing given to add")
    else:
        f = path.join(HOME, FILENAME)
        d = read_file(f)
        if d != None:
            d[nick] = (link, 0)
            json.dump(d, open(f, "w"))

def remove_fav(*args):
    f = path.join(HOME, FILENAME)
    try:
        nick = args[0]
    except IndexError:
        print("favorites: nothing given to remove")
    else:
        d = read_file(f)
        if d != None:
            try:
                del(d[nick])
            except KeyError:
                print("favorites: invalid name", nick)
            else:
                json.dump(d, open(f, "w"))

def list_favs(*args):
    f = path.join(HOME, FILENAME)
    d = read_file(f)
    if d != None:
        left_col = 0
        right_col = 0
        for nick in d:
            if len(nick) > left_col:
                left_col = len(nick)
            if len(d[nick]) > right_col:
                right_col = len(d[nick])
        for nick in d:
            print(format(nick, ">" + str(left_col)), "->",
                format(d[nick][0], "<" + str(right_col)), "(" + str(d[nick][1]) + ")")

def get_fav(nick = ""):
    f = path.join(HOME, FILENAME)
    d = read_file(f)
    if d != None:
        try:
            system("cd " + d[nick][0])
            d[nick][1] += 1
        except KeyError:
            print("favorites: invalid name", nick)
        except FileNotFoundError:
            print("favorites: invalid link")
        else:
            json.dump(d, open(f, "w"))

def main():
    options = {'add':add_fav, 'rm':remove_fav, 'remove':remove_fav, \
    'ls':list_favs, 'list':list_favs}
    if len(sys.argv) > 1:
        item = sys.argv[1]
        if item in options:
            try:
                options[item](*sys.argv[2:])
            except IndexError:
                options[item]()
        else:
            get_fav(item)
    else:
        print("Interactive mode")

if __name__ == '__main__':
    main()
