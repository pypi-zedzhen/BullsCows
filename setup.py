from setuptools import setup, find_packages
import BullsCows

setup(
    name='BullsCows',
    version=BullsCows.__version__,
    packages=find_packages(),
    url=BullsCows.__url__,
    license='zlib/libpng License',
    license_files='LICENSE',
    author=BullsCows.__author__,
    description='Игра в Быки-Коровы',
    install_requires=[
        'docopt==0.6.2',
        'colorama==0.4.4',
    ],
    python_requires='>=3.8',
    entry_points={
        'bc_symbols': [
            'ru = BullsCows.standard:ru',
            'en = BullsCows.standard:en',
            'di = BullsCows.standard:di',
        ],
        'console_scripts': [
            'BC = BullsCows.__main__:safe_main',
        ]
    }
)
