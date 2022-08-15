from typing import Union
from warnings import warn

from . import error, funcs
from .out import eprint, ok_print


def read_int(message: str = '', min_: int = None, max_: int = None):
    funcs.check_type(message, str, 'message')
    funcs.type_or_none(min_, int, 'min_')
    funcs.type_or_none(max_, int, 'max_')
    if funcs.notNone(min_) and funcs.notNone(max_) and min_ > max_:
        error.BCValueError('`min_` must be <= `max_`')
    number = None
    while number is None:
        try:
            number = int(funcs.input2(message))
        except ValueError:
            eprint('Необходимо ввести целое число!')
            continue
        if funcs.notNone(min_) and number < min_:
            eprint(f'Число должно быть не меньше {min_}')
            number = None
        elif funcs.notNone(max_) and number > max_:
            eprint(f'Число должно быть не больше {max_}')
            number = None
    return number


def read_int_str(value: Union[str, None], message_warn: str = '', message_input: str = '',
                 min_: int = None, max_: int = None):
    if value is None:
        return read_int(message_input, min_, max_)
    funcs.check_type(value, str, 'value')
    funcs.check_type(message_warn, str, 'message_warn')
    funcs.check_type(message_input, str, 'message_input')
    funcs.type_or_none(min_, int, 'min_')
    funcs.type_or_none(max_, int, 'max_')
    if funcs.notNone(min_) and funcs.notNone(max_) and min_ > max_:
        error.BCValueError('`min_` must be <= `max_`')
    try:
        number = int(value)
    except ValueError:
        warn(error.ValueWarn(f'Вы ввели не число ({message_warn})'))
        return read_int(message_input, min_, max_)

    if funcs.notNone(min_) and number < min_:
        warn(error.ValueWarn(f'Число должно быть не меньше {min_} ({message_warn})'))
        number = None
    elif funcs.notNone(max_) and number > max_:
        warn(error.ValueWarn(f'Число должно быть не больше {max_} ({message_warn})'))
        number = None

    if number is None:
        return read_int(message_input, min_, max_)
    return number


def read_symbols(pre_input: str = None, message: str = '') -> str:
    from .classes import SymbolsDict

    funcs.type_or_none(pre_input, str, 'pre_input')
    funcs.check_type(message, str, 'message')
    symbols = None
    k = 0
    while symbols is None:
        if funcs.notNone(pre_input):
            if k:
                k -= 1
            else:
                ok_print(pre_input)
                k = 15
        symbols = funcs.input2(message)
        symbols = SymbolsDict.unzip(symbols)
        if len(symbols) == 0:
            eprint('Была передана пустая строка символов')
            symbols = None
    return symbols


def read_symbols_str(value: Union[str, None], message_warn: str = '',
                     message_pre: str = None, message_input: str = ''):
    from .classes import SymbolsDict

    if value is None:
        return read_symbols(message_pre, message_input)
    funcs.check_type(value, str, 'value')
    funcs.check_type(message_warn, str, 'message_warn')
    funcs.check_type(message_pre, str, 'message_pre')
    funcs.check_type(message_input, str, 'message_input')

    symbols = SymbolsDict.unzip(value[1:])
    if len(symbols) == 0:
        warn(error.ValueWarn(f'Была передана пустая строка символов ({message_warn})'))
        return read_symbols(message_pre, message_input)
    return value
