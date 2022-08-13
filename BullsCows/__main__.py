import warnings

from .parse_argv import parse
from . import out, play
from .__init__ import __version__, __url__

COMMAND = {'play': play.main}


def main() -> None:
    warnings.showwarning = out.showwarning
    command, args = parse(__version__, f'Быки-Коровы ({__url__})')
    COMMAND[command](args)


def safe_main() -> None:
    try:
        main()
    except KeyboardInterrupt:
        out.eprint('Ctrl+C')
        exit(0)


if __name__ == '__main__':
    safe_main()
