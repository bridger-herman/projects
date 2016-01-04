#!/usr/bin/python3
import os
import sys
import re

# Takes 2 tuples
# Returns a tuple of (added, deleted)
def get_diff(new, old):
    added = []
    deleted = []
    same = []
    for x in new:
        if x not in old:
            added.append(x)
        else:
            if x not in same:
                same.append(x)
    for x in old:
        if x not in new:
            deleted.append(x)
        else:
            if x not in same:
                same.append(x)
    return (added, deleted, same)

# Check the sizes of files
def chk_sizes(new_path, old_path, lst):
    f_sizes = {}
    # Check for differences in size
    for f in lst:
        try:
            n_size = os.stat(new_path + "/" + f).st_size
        except FileNotFoundError:
            n_size = -1
        try:
            o_size = os.stat(old_path + "/" + f).st_size
        except FileNotFoundError:
            o_size = -1
        if n_size != o_size:
            f_sizes[f] = (n_size, o_size)
    return f_sizes

# Figure out whether or not to ignore a folder using Regex
def ignore(ign_list = [], path = ""):
    for pat in ign_list:
        if re.search(pat, path):
            return True
    return False

# Display the results
# Verbosity: 0 (display only number of files changed)
#   1 (display all files changed)
def display(paths = [], f_diff = [], s_diff = [], d_diff = [], ign_list = [], verb = 0):
    if len(paths) != len(f_diff) != len(paths) != len(d_diff):
        raise AttributeError("Mismatched Lengths")
    len_p = len(paths)

    print("Added files:")
    i = 0
    while i < len_p:
        if not ignore(ign_list, paths[i]):
            if verb == 1:
                for f in f_diff[i][0]:
                    print(" " + paths[i] + "/" + f)
            else:
                fcount = len(f_diff[i][0])
                if fcount != 0:
                    print(" " + paths[i] + ": " + str(fcount))
        i += 1
    print("\nDeleted files:")
    i = 0
    while i < len_p:
        if not ignore(ign_list, paths[i]):
            if verb == 1:
                for f in f_diff[i][1]:
                    print(" " + paths[i] + "/" + f)
            else:
                fcount = len(f_diff[i][1])
                if fcount != 0:
                    print(" " + paths[i] + ": " + str(fcount))
        i += 1
    # Find the maximum length of path + filename for formatting
    max_len = 0
    i = 0
    while i < len_p:
        if not ignore(ign_list, paths[i]):
            path_len = len(paths[i])
            if verb == 1:
                for f in s_diff[i]:
                    t_len = len(f) + path_len + 1
                    if t_len > max_len:
                        max_len = t_len
            else:
                if path_len + 1 > max_len:
                    max_len = path_len + 1
        i += 1
    print("\nChanged files:")
    if verb == 1:
        print(" " + format("File", ">" + str(max_len)) + format("New Size", ">14") + format("Old Size", ">14"))
    i = 0
    while i < len_p:
        if not ignore(ign_list, paths[i]):
            if verb == 1:
                for f in s_diff[i]:
                    print(" " + format(paths[i] + "/" + f, ">" + str(max_len)) + format(str(s_diff[i][f][0]), ">14") + format(str(s_diff[i][f][1]), ">14"))
            else:
                fcount = len(s_diff[i])
                if fcount != 0:
                    print(" " + format(paths[i] + ": " + str(fcount), ">" + str(max_len)))
        i += 1
    print("\nAdded directories:")
    i = 0
    while i < len_p:
        if not ignore(ign_list, paths[i]):
            for d in d_diff[i][0]:
                print(" " + paths[i] + "/" + d)
        i += 1
    print("\nDeleted directories:")
    i = 0
    while i < len_p:
        if not ignore(ign_list, paths[i]):
            for d in d_diff[i][1]:
                print(" " + paths[i] + "/" + d)
        i += 1

# Command line arguments:
# ./treediff.py <new_path> <old_path> <verbosity> <dirs to ignore>
# Must put "" around regexes
def main():
    try:
        new_i = os.walk(sys.argv[1])
        old_i = os.walk(sys.argv[2])
    except IndexError:
        raise AttributeError("Incorrect number of parameters")
    try:
        ign = sys.argv[3].split(",")
    except IndexError:
        ign = []
    try:
        verb = int(sys.argv[4])
    except IndexError:
        verb = 0
    len_np = len(sys.argv[1])
    len_op = len(sys.argv[2])
    # Differences in added/deleted files
    file_diffs = []
    # In files that are same, is size changed?
    size_diffs = []
    # Difference in added/deleted directories
    dir_diffs = []
    paths = []
    done = False
    i = 0
    while not done:
        try:
            # (dirpath, dirnames, filenames)
            new = next(new_i)
            old = next(old_i)
            # This is to prevent different directories from being compared
            new[1].sort()
            old[1].sort()
            # Full path
            new_p = new[0]
            old_p = old[0]
            # Full initial path
            new_pi = new[0]
            old_pi = old[0]
            # This is to prevent toplevel directory mismatches for added directories
            # Compares relative paths to make sure they're the same
            while new_p[len_np:] != old_p[len_op:]:
                if re.search(new_pi, new_p):
                    file_diffs.append((new[2], [], []))
                    dir_diffs.append((new[1], [], []))
                    size_diffs.append({})
                    paths.append(new_p[len_np:])
                    new = next(new_i)
                    new[1].sort()
                    new_p = new[0]
                else:
                    file_diffs.append(([], old[2], []))
                    dir_diffs.append(([], old[1], []))
                    size_diffs.append({})
                    paths.append(old_p[len_op:])
                    old = next(old_i)
                    old[1].sort()
                    old_p = old[0]
                # print(new_p[len_np:])
                # print(old_p[len_op:])
                # input()
            # Add (added, deleted, same) files
            file_diffs.append(get_diff(new[2], old[2]))
            # Add modified file sizes
            # {file: (new_size, old_size) ...}
            size_diffs.append(chk_sizes(new_p, old_p, file_diffs[-1][2]))
            # Add (added, deleted, same) directories
            dir_diffs.append(get_diff(new[1], old[1]))
            # Add the current paths
            paths.append(new_p[len_np:])
        except StopIteration:
            done = True
        # print("\x1b[1;35mfile_diffs\x1b[0m", file_diffs[i])
        # print("\x1b[1;34msize_diffs\x1b[0m", size_diffs[i])
        # print("\x1b[1;36mdir_diffs\x1b[0m", dir_diffs[i])
        # print("\x1b[1;32mpaths\x1b[0m", paths[i])
        i += 1
    display(paths, file_diffs, size_diffs, dir_diffs, ign, verb)

if __name__ == '__main__':
    main()
