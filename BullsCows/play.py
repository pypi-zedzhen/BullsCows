from . import funcs
from .error import WrongStr
from .lower_api import create_game
from .out import eprint


def main(args):
    game = create_game(args)
    game.start()
    while not game.win:
        s = funcs.input2('Ваша последовательность: ')
        try:
            print(game.trying(s))
        except WrongStr:
            eprint('Некорректная строка')
    print('Поздравляем, Вы выиграли!')
    print(f"(за {game.count} ход{ {1: '', 2: 'а', 3: 'ов'}[funcs.finish_word(game.count)]})")
