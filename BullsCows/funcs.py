from typing import ClassVar, Any, Union
from warnings import warn

from colorama import Fore

from . import error
from .out import color_print, eprint


def check_type(value: Any, class_: ClassVar, str_value: str, str_class: str = None) -> None:
    if not isinstance(class_, type):
        raise error.BCTypeError.one('class_', 'class', class_)
    if not isinstance(str_value, str):
        raise error.BCTypeError.one('str_value', 'str', str_value)
    if str_class is None:
        str_class = class_.__name__
    if not isinstance(str_class, str):
        raise error.BCTypeError.one('str_class', 'str', str_class)

    if not isinstance(value, class_):
        raise error.BCTypeError.one(str_value, str_class, value)


def type_or_none(value: Any, class_: ClassVar, str_value: str, str_class: str = None) -> None:
    if value is not None:
        check_type(value, class_, str_value, str_class)


def input2(message: str = '') -> str:
    try:
        return input(message)
    except EOFError:
        warn(error.EOFWarn())
        exit(2)


def finish_word(int_: int) -> int:
    check_type(int_, int, 'int_')
    int_ = abs(int_)
    if 5 <= int_ <= 20 or int_ % 10 >= 5 or int_ % 10 == 0:
        return 3
    if int_ % 10 == 1:
        return 1
    return 2


# noinspection PyPep8Naming
def notNone(value: Any) -> bool:
    return value is not None


def read_int(message: str = '', min_: int = None, max_: int = None):
    check_type(message, str, 'message')
    type_or_none(min_, int, 'min_')
    type_or_none(max_, int, 'max_')
    if notNone(min_) and notNone(max_) and min_ > max_:
        error.BCValueError('`min_` must be <= `max_`')
    number = None
    while number is None:
        try:
            number = int(input2(message))
        except ValueError:
            eprint('Необходимо ввести целое число!')
        if notNone(min_) and number < min_:
            eprint(f'Число должно быть не меньше {min_}')
            number = None
        elif notNone(max_) and number > max_:
            eprint(f'Число должно быть не больше {max_}')
            number = None
    return number


def read_int_str(value: Union[str, None], message_warn: str = '', message_input: str = '',
                 min_: int = None, max_: int = None):
    if value is None:
        return read_int(message_input, min_, max_)
    check_type(value, str, 'value')
    check_type(message_warn, str, 'message_warn')
    type_or_none(min_, int, 'min_')
    type_or_none(max_, int, 'max_')
    if notNone(min_) and notNone(max_) and min_ > max_:
        error.BCValueError('`min_` must be <= `max_`')
    try:
        number = int(value)
    except ValueError:
        warn(error.ValueWarn(f'Вы ввели не число ({message_warn})'))
        return read_int(message_input, min_, max_)

    if notNone(min_) and number < min_:
        warn(error.ValueWarn(f'Число должно быть не меньше {min_} ({message_warn})'))
        number = None
    elif notNone(max_) and number > max_:
        warn(error.ValueWarn(f'Число должно быть не больше {max_} ({message_warn})'))
        number = None

    if number is None:
        return read_int(message_input, min_, max_)
    return number


def read_symbols(pre_input: str = None, message: str = '') -> str:
    from .classes import SymbolsDict

    type_or_none(pre_input, str, 'pre_input')
    check_type(message, str, 'message')
    symbols = None
    k = 0
    while symbols is None:
        if notNone(pre_input):
            if k:
                k -= 1
            else:
                color_print(Fore.GREEN, pre_input)
                k = 15
        symbols = input2(message)
        if len(symbols) == 0:
            eprint('Была передана пустая строка символов')
            symbols = None
            continue
        elif symbols[0] == '_':
            symbols = SymbolsDict.unzip(symbols[1:])
            if len(symbols) == 0:
                eprint('Была передана пустая строка символов')
                symbols = None
    return symbols


def read_symbols_str(value: Union[str, None], message_warn: str = '',
                     message_pre: str = None, message_input: str = ''):
    from .classes import SymbolsDict

    if value is None:
        return read_symbols(message_pre, message_input)
    check_type(value, str, 'value')
    check_type(message_warn, str, 'message_warn')

    if len(value) == 0:
        warn(error.ValueWarn(f'Была передана пустая строка символов ({message_warn})'))
        return read_symbols(message_pre, message_input)
    elif value[0] == '_':
        symbols = SymbolsDict.unzip(value[1:])
        if len(symbols) == 0:
            warn(error.ValueWarn(f'Была передана пустая строка символов ({message_warn})'))
            return read_symbols(message_pre, message_input)
    return value
