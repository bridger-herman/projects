# Idea from http://effbot.org/librarybook/readline.htm
import readline

class Completer:
    # completer is a function of the form completer(self, prefix, index)
    def __init__(_, completer = None):
        _.__old_completer = readline.get_completer()
        _.__old_delims = readline.get_completer_delims()
        readline.set_completer_delims(' \t\n;')
        readline.parse_and_bind("tab: complete")
        readline.set_completer(completer)

    def reset(_):
        readline.set_completer_delims(_.__old_delims)
        readline.set_completer(_.__old_completer)

    def input(_, phrase = ""):
        return input(phrase)
