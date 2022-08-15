from typing import Any, ClassVar
from warnings import warn

from . import error


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
