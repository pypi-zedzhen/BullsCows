import sys

from colorama import Fore, Style


def color_print(color, *values, sep=' ', end='\n', file=sys.stderr, flush=False):
    print(color, end='')
    print(*values, sep=sep, end=end, file=file, flush=flush)
    print(Style.RESET_ALL, end='')


def eprint(*values, sep=' ', end='\n', flush=False):
    color_print(Fore.RED, *values, sep=sep, end=end, flush=flush)


def ok_print(*values, sep=' ', end='\n', flush=False):
    color_print(Fore.GREEN, *values, sep=sep, end=end, file=sys.stdout, flush=flush)


def showwarning(message, category, *_):
    color_print(Fore.YELLOW, f'{category.__name__}: {message}')
