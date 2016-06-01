#!/usr/bin/env python
from distutils.core import setup
from setuptools import find_packages

setup(
    name='ParallelDownload',
    version='0.07',
    description='A library to download large files in chunks.',
    author='Halil Ozercan',
    author_email='halilozercan@gmail',
    url='https://github.com/halilozercan/paralleldownload',
    download_url = 'https://github.com/halilozercan/paralleldownload/tarball/0.07',
    entry_points={
        'console_scripts': [
            'pdownload = ParallelDownload.bin:main',
        ],
    },
    install_requires=['requests', 'wheel'],
    packages=find_packages(exclude=("tests", "tests.*")),
)
