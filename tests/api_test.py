from __future__ import unicode_literals
# Remain to be filled with test cases.
from pget import Downloader

import sys


def sha1sum(file_name):
    import hashlib
    BUF_SIZE = 65536

    sha1 = hashlib.sha1()

    with open(file_name, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            sha1.update(data)

    return sha1.hexdigest()


downloader = Downloader('http://halilibo.com/filez/i/StfyyS6.mp4', 'video.mp4', 8)
downloader.start_sync()

assert sha1sum('video.mp4') == '5298b02a64cb4ed7cc6e617b0cc2f0b4b36afb6a'