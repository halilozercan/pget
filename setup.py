#!/usr/bin/env python
from distutils.core import setup
from setuptools import find_packages

setup(
    name='PGet',
    version='0.4',
    description='A tool and library to save large files by creating multiple connections.',
    author='Halil Ozercan',
    author_email='halilozercan@gmail',
    url='https://github.com/halilozercan/pget',
    download_url='https://github.com/halilozercan/pget/tarball/0.4',
    entry_points={
        'console_scripts': [
            'pget = pget.bin:main',
        ],
    },
    install_requires=['requests', 'wheel'],
    packages=find_packages(exclude=("tests", "tests.*")),
)
