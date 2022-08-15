import os
import pickle
import warnings
from os import listdir, makedirs, path
from secrets import randbelow
from sys import exit
from time import time

from . import error, funcs, lower_api
from .classes import Game
from .const import DIRECTORY, EXTENSION
from .out import eprint, ok_print


def new(args) -> None:
    game = lower_api.create_game(args)
    dump = pickle.dumps(game, pickle.HIGHEST_PROTOCOL)

    try:
        makedirs(args['--dir'], exist_ok=True)
    except OSError as e:
        eprint(f'Ошибка сохранения ({e})')

    if args['--name'] is None:
        s = set(listdir(args['--dir']))
        while True:
            name = f'BC_{randbelow(10 ** 5)}_{int(time()) % (10 ** 5)}{EXTENSION}'
            if name not in s:
                args['--name'] = name
                break

    if not args['--no-extension'] and not args['--name'].endswith(EXTENSION):
        args['--name'] += EXTENSION

    filename = path.join(args['--dir'], args['--name'])
    try:
        lower_api.save(dump, filename, args['-f'])
    except error.BCFileExistsError as e:
        eprint(f'Используйте -f для перезаписи  ({e})')
        exit(1)
    except error.BCError as e:
        eprint(f'Ошибка сохранения ({e})')
        exit(1)
    ok_print(f'''Игра создана.
Файл: {filename}''')
    if args['--start']:
        print()
        args['<filename>'] = filename
        start(args)


def start(args) -> None:
    filename = args['<filename>']
    if not path.exists(filename):
        f2 = filename + EXTENSION
        f3 = path.join('.', DIRECTORY, filename)
        f4 = path.join('.', DIRECTORY, filename + EXTENSION)
        if path.exists(f2):
            warnings.warn(error.ValueWarn(f'Файл {filename} не найден, используется {f2}'))
            filename = f2
        elif path.exists(f3):
            warnings.warn(error.ValueWarn(f'Файл {filename} не найден, используется {f3}'))
            filename = f3
        elif path.exists(f4):
            warnings.warn(error.ValueWarn(f'Файл {filename} не найден, используется {f4}'))
            filename = f4
        else:
            eprint(f'Файл {filename} не найден (в том числе {f2}, {f3}, {f4})')
            exit(1)

    try:
        data = lower_api.read(filename)
    except error.BCError as e:
        eprint(e)
        exit(1)

    try:
        # noinspection PyUnboundLocalVariable
        game = pickle.loads(data)
        funcs.check_type(game, Game, '')
    except (pickle.PickleError, error.BCTypeError):
        eprint(f"файл `{filename}` повреждён")
        exit(1)

    pause_s = 'pause'
    # noinspection PyUnboundLocalVariable
    if game.len == len(pause_s):
        pause_s += '_'
    ok_print(f"Для выхода введите `{pause_s}`")
    game.start()
    saved = True
    while not game.win:
        s = funcs.input2('Ваша последовательность: ')
        if s == pause_s:
            if saved:
                return
            try:
                lower_api.save(pickle.dumps(game), filename, True)
            except error.BCError as e:
                eprint(f'Не удалось сохранить ({e})')
        try:
            print(game.trying(s))
        except error.WrongStr:
            eprint('Некорректная строка')
        try:
            lower_api.save(pickle.dumps(game), filename, True)
            saved = True
        except error.BCError:
            saved = False
    ok_print('Поздравляем, Вы выиграли!')
    ok_print(f"(за {game.count} ход{ {1: '', 2: 'а', 3: 'ов'}[funcs.finish_word(game.count)]})")
    if args['--delete']:
        try:
            os.remove(filename)
        except OSError as e:
            eprint(f'Не удалось удалить файл ({e})')
            exit(1)
