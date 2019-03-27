#!/usr/bin/env python3

from distutils.core import setup

setup(
    name='facebookcli',
    version='1.0',
    description='Facebook command line interface using selenium to emulate human behavior',
    author='Matteus Magnusson',
    author_email='matteus.magnusson@gmail.com',
    url='https://github.com/Senth/facebook-cli',
    packages='facebookcli',
    entry_points={
        'console_scripts': [
            'facebookcli=facebookcli.__main__:__main__'
        ],
    },
    install_requires=[
        'selenium',
        'mysqlclient'
    ],
)
