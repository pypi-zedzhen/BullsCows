from os import makedirs, path

from .classes import Game, SymbolsDict
from .error import BCError, BCFileExistsError
from .funcs import check_type
from .read import read_int_str, read_symbols_str


def create_game(args):
    len_ = read_int_str(args['--len'], 'параметр `--len`',
                        'Введите длину последовательности: ', min_=1)
    s = r'''Если вы хотите добавить `_` введите `/_`, для `/` - `//`''' + '\n'
    for key, value in SymbolsDict.load().items():
        s += f'_{key} - {value.about}\n'
    if args['--case-sensitive']:
        s += '''Используйте CAPS версию для больших букв\n'''
    symbols = read_symbols_str(args['--symbols'], 'параметр `--symbols`', s[:-1], 'Введите символы: ')
    return Game(len_, symbols, args['--case-sensitive'])


def save(data: bytes, filename: str, force: bool) -> None:
    check_type(data, bytes, 'data')
    check_type(filename, str, 'filename')
    check_type(force, bool, 'force')

    if path.exists(filename) and not force:
        raise BCFileExistsError(f"Путь `{filename}` уже существует")

    try:
        makedirs(path.dirname(filename), exist_ok=True)
        with open(filename, mode='wb') as f:
            f.write(data)
    except OSError as e:
        raise BCError(f"Не удалось записать в файл `{filename}` (ошибка: {str(e)})")


def read(filename: str) -> bytes:
    try:
        with open(filename, 'rb') as f:
            return f.read()
    except OSError as e:
        raise BCError(f"Не удалось прочитать файл `{filename}` (ошибка: {str(e)})")
