from .completer import Completer

class ListCompleter(Completer):
    def __init__(_, items = None):
        super().__init__(_.__complete)
        if items == None:
            _.__items = []
        else:
            _.__items = items
        _.__prefix = None
        _.__matches = None

    def __complete(_, prefix, index):
        if prefix != _.__prefix:
            _.__matches = [i for i in _.__items if i.startswith(prefix)]
            _.__prefix = prefix
        try:
            return _.__matches[index]
        except IndexError:
            return None
