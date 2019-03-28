#!/usr/bin/env python3

from distutils.core import setup

setup(
    name='facebookcli',
    version='1.0.0',
    description='Facebook command line interface using selenium to emulate human behavior',
    author='Matteus Magnusson',
    author_email='senth.wallace@gmail.com',
    url='https://github.com/Senth/facebook-cli',
    packages=['facebookcli'],
    package_data={'':'help-description'},
    include_package_data=True,
    data_files=[
        ('config/facebookcli/', ['config/config.example.py']),
    ],
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
