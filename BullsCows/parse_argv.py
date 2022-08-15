from os.path import join
from sys import argv, exit
from typing import Any, Union

from docopt import docopt

from .__init__ import __version__
from .classes import BCStr
from .const import DIRECTORY, EXTENSION
from .error import BCTypeError
from .funcs import check_type
from .out import eprint


class Translate:
    def __init__(self, dict_en2ru: dict[str, str] = None):
        if dict_en2ru is None:
            self.dict = {}
        else:
            self.dict = dict_en2ru

    def en2ru(self, doc: str) -> BCStr:
        check_type(doc, str, 'doc')
        if isinstance(doc, str):
            doc = BCStr(doc)

        for en, ru in self.dict.items():
            doc = doc.replace2(en, ru)
        return doc

    def ru2en(self, doc: str) -> BCStr:
        check_type(doc, str, 'doc')
        if isinstance(doc, str):
            doc = BCStr(doc)

        for en, ru in self.dict.items():
            doc = doc.replace2(ru, en)
        return doc


class HelpStr(str):
    def __str__(self):
        s = self
        while s[0] in (' ', '\n', '\t'):
            s = s[1:]
        while s[-1] in (' ', '\n', '\t'):
            s = s[:-1]
        return s


class Help:
    default_translate = Translate(
        {
            'Usage': 'Использование',
            'Options': 'Параметры',
            'Default': 'По умолчанию',
            'Command': 'Команда',
        }
    )

    def __init__(self, message_ru: str, translate: Translate = default_translate):
        self.ru = HelpStr(message_ru)
        self.en = HelpStr(translate.ru2en(message_ru))


class DictCommand(dict[str, Help]):
    def __init__(self, commands: dict[str, Union[Help, str]] = None):
        super().__init__()
        if commands is None:
            return

        check_type(commands, dict, 'commands')
        for key, value in commands.items():
            self[key] = value

    def __setitem__(self, key: str, value: Union[Help, str]):
        check_type(key, str, 'key')
        if isinstance(value, str):
            value = Help(value)
        if not isinstance(value, Help):
            raise BCTypeError.two('value', ('str', 'Help'), value)
        super().__setitem__(key, value)

    def __missing__(self, key: str):
        check_type(key, str, 'key')
        err_parse(f'команды `{key}` нет')


main = Help("""
Использование:
    BC -h | --help              Для вывода этого сообщения
    BC -V | --version           Для получения версии
    BC --new                    Что нового в версии
    BC <команда> (-h | --help)  Справка по команде
    BC <команда> [параметры]    Для использования команды

вместо "BC" можно использовать "python -m BC"

Параметры:
    -h --help            Это сообщение
    -V --version         Версия программы

Команды:
    play       запуск игры в Быки-Коровы
    new_game   создание новой игры
    play_game  Запуск существующей игры
""")

COMMANDS = DictCommand(
    {
        'play': """
Использование:
    BC play -h | --help
    BC play [--len=<len>] [--symbols=<symbols>] [--case-sensitive]

Параметры:
    -h --help             Это сообщение
    --len=<len>           Длина последовательности
    --symbols=<symbols>   Допустимые символы
    -c, --case-sensitive  Регистрозависимая игра
""",
        'new_game': f"""
Использование:
    BC new_game -h | --help
    BC new_game [--len=<len>] [--symbols=<symbols>] [--case-sensitive] 
                [--dir=<dir>] [--name=<name> [-f] [-E | --no-extension]] [-s | --start [-d | --delete]]

Параметры:
    -h --help             Это сообщение
    --len=<len>           Длина последовательности
    --symbols=<symbols>   Допустимые символы
    -c, --case-sensitive  Регистрозависимая игра
    --dir=<dir>           Директория для сохранения [по умолчанию: {join('.', DIRECTORY)}]
    --name=<name>         Имя сохранения
    -f                    Перезаписать файл
    -E, --no-extension    Не добавлять расширение {EXTENSION} (по умолчанию добавляется, если нет)

    -s, --start           Запустить игру
    -d, --delete          Удалить файл игры после выигрыша
""",
        'play_game': """
Использование:
    BC play_game -h | --help
    BC play_game <filename> [-d | --delete]

Параметры:
    -h --help     Это сообщение
    <filename>    Файл сохранения игры
    -d, --delete  Удалить файл игры после выигрыша
""",
    }
)


def err_parse(message: str = '', help_: Help = main):
    check_type(message, str, 'message')
    check_type(help_, Help, 'help_')
    if message != '':
        message = ': ' + message
    eprint('Неправильное использование' + message)
    print(help_.ru)
    exit(1)


def parse(prog_name: str = '') -> tuple[str, dict[str, Any]]:
    if prog_name:
        prog_name += '\n'
    else:
        prog_name = ''

    if len(argv) == 1:
        err_parse('нет параметров')
    command = argv[1]
    if command in ('-h', '--help'):
        print(main.ru)
        exit(0)
    if command in ('-V', '--version'):
        print(f"{prog_name}Версия: {__version__}")
        exit(0)
    if command == '--new':
        print(f"""Что нового в версии `{__version__}`:
1) Добавлена эта команда (флаг `--new`)
2) Добавлены команды `new_game` и `play_game`
3) Изменён вариант выбора символов (подробнее в README)
""")
        exit(0)

    help_ = COMMANDS[command]
    try:
        args = dict(docopt(help_.en, help=False))
    except SystemExit:
        err_parse(help_=help_)
    # noinspection PyUnboundLocalVariable
    if args['--help']:
        print(help_.ru)
        exit(0)
    return command, args
