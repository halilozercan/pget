from __future__ import print_function

import sys

from ParallelDownload import Downloader


def download_callback(downloader):
    sys.stdout.write("\rDownloading %s [%s] [%s]" %
                     (downloader.file_name, 100 * (float(downloader.total_downloaded) / downloader.total_length),
                      downloader.readable_speed))
    sys.stdout.flush()


def main():
    if sys.stdin.isatty():
        downloader = Downloader(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        argv = sys.stdin.read().split(' ')
        downloader = Downloader(argv[1], argv[2], argv[3])

    downloader.subscribe(download_callback)

    downloader.start()

    downloader.wait_for_finish()
