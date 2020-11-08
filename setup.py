#!/usr/bin/env python3

from setuptools import setup

setup(
    name="facebookcli",
    version="1.0.1",
    description="Automatically post birthday wishes and schedule Facebook Messenger messages from the command line.",
    author="Matteus Magnusson",
    author_email="senth.wallace@gmail.com",
    url="https://github.com/Senth/facebook-cli",
    packages=["facebookcli"],
    package_data={"facebookcli": ["help-description"]},
    include_package_data=True,
    data_files=[
        ("config/facebookcli/", ["config/config.example.py"]),
    ],
    entry_points={
        "console_scripts": ["facebookcli=facebookcli.__main__:main"],
    },
    install_requires=["selenium", "mysqlclient"],
)
