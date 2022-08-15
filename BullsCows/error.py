from typing import Any


class BCError(Exception):
    pass


class BCWarn(Warning):
    pass


class BCTypeError(BCError, TypeError):
    @classmethod
    def one(cls, param_name: str, correct_class: str, param: Any):
        return cls(f'`{param_name}` must be `{correct_class}`, not `{type(param).__name__}`')

    @classmethod
    def two(cls, param_name: str, correct_class: tuple[str, str], param: Any):
        return cls(f'`{param_name}` must be `{correct_class[0]}` or `{correct_class[1]}`, not `{type(param).__name__}`')


class BCFileExistsError(BCError, FileExistsError):
    pass


class BCValueError(BCError, ValueError):
    pass


class GameNotStart(BCError):
    pass


class WrongStr(BCError, ValueError):
    pass


class NotFound(BCWarn):
    pass


class ValueWarn(BCWarn):
    pass


class EOFWarn(BCWarn):
    def __init__(self, message='Конец потока'):
        super().__init__(message)


class AddLenWarn(BCWarn):
    D_MESSAGE = 'Неправильная длина, одного из дополнений'

    def __init__(self, message=D_MESSAGE):
        super().__init__(message)

    @classmethod
    def comment(cls, comment: str):
        if not isinstance(comment, str):
            raise BCTypeError.one('comment', 'str', comment)
        return cls(f"{cls.D_MESSAGE}: {comment}")
