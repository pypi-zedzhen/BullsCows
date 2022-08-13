from sys import stderr

from colorama import Fore, Style


def color_print(color, *args, **kw):
    print(color, end='')
    print(*args, file=stderr, **kw)
    print(Style.RESET_ALL, end='')


def eprint(*args, **kw):
    color_print(Fore.RED, *args, **kw)


def showwarning(message, category, *_):
    color_print(Fore.YELLOW, f'{category.__name__}: {message}')
