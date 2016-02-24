from .completer import Completer
from pathlib import Path

class FilePathCompleter(Completer):
    def __init__(_, root_dir = "."):
        super().__init__(_.__completer)
        _.__prefix = ""
        _.__current_dir = Path(root_dir)
        _.__items = None
        _.__matches = None
        _.__update_contents()


    def __completer(_, prefix, index):
        f = open("out.txt", "a")
        print(prefix, _.__current_dir, file = f)
        f.close()
        # Options:
        # move to a subdirectory (if prefix has a full match)
        # move to a parent directory (if current directory is no longer in prefix)
        # stay where we are
        if prefix != _.__prefix:
            _.__matches = [d for d in _.__items if str(d).startswith(prefix)]
            _.__prefix = prefix
        # Hard-coded prefix path supersedes tab-completed path
        # pre_path = Path(prefix)
        # if pre_path.is_dir():
        #     _.__current_dir = pre_path
        #     _.__update_contents()
        #     return str(pre_path)
        try:
            chosen = _.__matches[index]
            if chosen.is_dir():
                _.__current_dir /= chosen
                _.__update_contents()
            return str(_.__matches[index])
        except IndexError:
            return None

    def __update_contents(_):
        _.__items = [i for i in _.__current_dir.iterdir()]
        # print(" ".join([str(d) for d in _.__dir_list]))
        # print(" ".join([str(f) for f in _.__file_list]))

    # Given a root directory.
    # Directory path: walk[0]
    # Directory list: walk[1]
    # File list: walk[2]
    #
    # Given an input: if it's in the dir list, change self.root_dir to subdir
    # Else, we're done
    # Need some way to keep track of nesting and when we need to back out.
