from .classes import Game, SymbolsDict
from . import funcs
from .error import WrongStr
from .out import eprint


def main(args):
    len_ = funcs.read_int_str(args['--len'], 'параметр `--len`',
                              'Введите длину последовательности: ', min_=1)
    s = '''Для встроенных наборов поставьте `_` первым символов (можно комбинировать)\n'''
    for key, value in SymbolsDict.load().items():
        s += f'{key} - {value.about}\n'
    if args['--case-sensitive']:
        s += '''Используйте CAPS версию для больших букв\n'''
    symbols = funcs.read_symbols_str(args['--symbols'], 'параметр `--symbols`', s[:-1], 'Введите символы: ')

    game = Game(len_, symbols, args['--case-sensitive'])
    game.start()
    while not game.win:
        s = funcs.input2('Ваша последовательность: ')
        try:
            print(game.trying(s))
        except WrongStr:
            eprint('Некорректная строка')
    print('Поздравляем, Вы выиграли!')
    print(f"(за {game.count} ход{ {1: '', 2: 'а', 3: 'ов'}[funcs.finish_word(game.count)]})")
