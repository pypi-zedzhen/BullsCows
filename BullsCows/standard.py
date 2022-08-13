from string import ascii_lowercase, digits

from .classes import StandardSymbol

ru = StandardSymbol('абвгдеёжзийклмнопрстуфхцчшщъыьэюя', 'русские буквы')
en = StandardSymbol(ascii_lowercase, 'английские буквы')
di = StandardSymbol(digits, 'цифры', case_sensitive=False)
