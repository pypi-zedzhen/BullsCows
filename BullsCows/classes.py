import secrets
from dataclasses import dataclass
from warnings import warn

from pkg_resources import iter_entry_points

from . import error
from .funcs import check_type


class BCStr(str):
    def replace(self, old: str, new: str, count: int = -1) -> 'BCStr':
        return type(self)(super().replace(old, new, count))

    def replace_dict(self, d: dict[str, str]) -> 'BCStr':
        s = self
        for old, new in d.items():
            s = s.replace2(old, new)
        return s

    def replace2(self, old: str, new: str):
        s = self.replace(old, new)
        for f in (str.capitalize, str.lower, str.title, str.upper):
            # noinspection PyArgumentList
            s = s.replace(f(old), f(new))
        return s


class BCDict(dict[str, int]):
    def __init__(self, d: dict = None):
        super().__init__()
        if d is not None:
            check_type(d, dict, 'd')
            for key, value in d.items():
                self[key] = value

    def __missing__(self, key: str):
        check_type(key, str, 'key')
        self[key] = 0
        return 0

    def __setitem__(self, key: str, value: int) -> None:
        check_type(key, str, 'key')
        check_type(value, int, 'value')
        super().__setitem__(key, value)

    def intersection(self, other: 'BCDict') -> 'BCDict':
        check_type(other, BCDict, 'other')
        inter = BCDict()
        for key, value in self.items():
            min_value = min(value, other[key])
            if min_value:
                inter[key] = min_value
        return inter

    def sum(self) -> int:
        return sum(self.values())


@dataclass(eq=False)
class StandardSymbol:
    symbols: str
    about: str
    symbols_upper: str = None
    case_sensitive: bool = True

    def __post_init__(self):
        if self.case_sensitive and self.symbols_upper is None:
            self.symbols_upper = self.symbols.upper()


class SafeStr(str):
    def __getitem__(self, item):
        try:
            return super().__getitem__(item)
        except IndexError:
            return ''


class SymbolsDict(dict[str, StandardSymbol]):
    LEN = 2

    def __init__(self, d: dict = None):
        super().__init__()
        if d is not None:
            check_type(d, dict, 'd')
            for key, value in d.items():
                self[key] = value

    def get_symbols(self, key: str):
        check_type(key, str, 'key')
        if key in self.keys():
            return self[key].symbols
        elif key.isupper():
            lower_key = key.lower()
            if lower_key in self.keys():
                lower = self[lower_key]
                if lower.case_sensitive:
                    return lower.symbols_upper
                return lower.symbols
        warn(error.NotFound(f'значение для `{key}` не найдено'))
        return ''

    def __setitem__(self, key: str, value: StandardSymbol) -> None:
        check_type(key, str, 'key')
        check_type(value, StandardSymbol, 'value')
        super().__setitem__(key, value)

    @classmethod
    def load(cls) -> 'SymbolsDict':
        symbols = cls()
        for entry_point in iter_entry_points('bc_symbols'):
            symbol = entry_point.load()
            if isinstance(symbol, StandardSymbol):
                try:
                    symbols[entry_point.name] = symbol
                except error.BCValueError:
                    warn(error.AddLenWarn.comment(f'длина ключа не равна {cls.LEN} ({entry_point.name})'))
        return symbols

    @classmethod
    def unzip(cls, zip_str: str) -> str:
        check_type(zip_str, str, 'zip_str')
        zip_str = SafeStr(zip_str)

        d = cls.load()
        unzip_str = ''
        i = 0
        while i < len(zip_str):
            char = zip_str[i]
            if char == '/':
                unzip_str += zip_str[i + 1]
                i += 2
                continue
            if char != '_':
                unzip_str += char
                i += 1
                continue
            if zip_str[i + 1] != '_':
                key = zip_str[i + 1:i + cls.LEN + 1]
                unzip_str += d.get_symbols(key)
                i += cls.LEN + 1
                continue
            i += 2
            key = ''
            while zip_str[i] != '_':
                if i == len(zip_str):
                    warn(error.ValueWarn(f'in `zip_str`, not end key (begin key `{key}`)'))
                    break
                key += zip_str[i]
                i += 1
            else:
                i += 1
                unzip_str += d.get_symbols(key)
        return unzip_str


@dataclass(eq=False)
class Result:
    bulls: int
    cows: int

    def __post_init__(self):
        check_type(self.bulls, int, 'bulls')
        check_type(self.cows, int, 'cows')

    # noinspection PyShadowingBuiltins
    def __str__(self, format: BCStr = BCStr('Быков: %b, Коров %c')):
        check_type(format, BCStr, 'format')
        return format.replace_dict({'%b': str(self.bulls),
                                    '%c': str(self.cows)})


class Game:
    def __init__(self, len_: int, symbols: str, case_sensitive: bool):
        check_type(len_, int, 'len')
        check_type(symbols, str, 'symbols')
        check_type(case_sensitive, bool, 'case_sensitive')
        if len_ <= 0:
            raise error.BCValueError(f'`len_` must be >=1, not {len_}')
        self.len = len_
        if not case_sensitive:
            symbols = symbols.lower()
        self.symbols = symbols
        self.case_sensitive = case_sensitive
        self.started = False
        self.win = False
        self.count = 0

        self.ans = None

    def start(self) -> None:
        if self.started or self.win:
            return
        self.started = True
        self.ans = self.gen()
        if not self.case_sensitive:
            self.ans = self.ans.lower()
        if not self.check_str(self.ans):
            raise error.BCError('error in gen correct answer')

    def gen(self) -> str:
        s = ''
        for _ in range(self.len):
            s += secrets.choice(self.symbols)
        return s

    def check_str(self, s: str) -> bool:
        if not isinstance(s, str):
            return False
        if len(s) != self.len:
            return False
        for i in s:
            if i not in self.symbols:
                return False
        return True

    def trying(self, user_str: str) -> Result:
        check_type(user_str, str, 'user_str')
        if not self.started:
            raise error.GameNotStart

        if not self.case_sensitive:
            user_str = user_str.lower()

        if not self.check_str(user_str):
            raise error.WrongStr

        res = self.get_bulls_cows(user_str)
        if res.bulls == self.len:
            self.win = True
            self.started = False
        self.count += 1

        return res

    def get_bulls_cows(self, user_str: str) -> Result:
        check_type(user_str, str, 'user_str')
        bulls = 0
        ans_new = BCDict()
        user_new = BCDict()
        for i in range(self.len):
            correct = self.ans[i]
            user = user_str[i]
            if correct == user:
                bulls += 1
            else:
                ans_new[correct] += 1
                user_new[user] += 1
        cows = ans_new.intersection(user_new).sum()
        return Result(bulls, cows)
