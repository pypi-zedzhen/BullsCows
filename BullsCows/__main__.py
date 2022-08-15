import warnings

from . import api, out, play
from .__init__ import __url__
from .parse_argv import parse

COMMAND = {'play': play.main,
           "new_game": api.new,
           "play_game": api.start}


def main() -> None:
    warnings.showwarning = out.showwarning
    command, args = parse(f'Быки-Коровы ({__url__})')
    out.eprint(args)
    COMMAND[command](args)


def safe_main() -> None:
    try:
        main()
    except KeyboardInterrupt:
        out.eprint('Ctrl+C')
        exit(0)


if __name__ == '__main__':
    safe_main()
