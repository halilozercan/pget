import sys

import signal
from ParallelDownload import Downloader


def download_callback(downloader):
    sys.stdout.write("\rDownloading\t%s\t[%s]\t[%s]\t%s\t%s" %
                     (downloader.file_name, 100 * (float(downloader.total_downloaded) / downloader.total_length),
                      downloader.readable_speed, downloader.total_downloaded, downloader.total_length))
    sys.stdout.flush()


def run(argv):

    def handler(signum, frame):
        if signum == signal.SIGKILL:
            print 'SIGKILL'
        elif signum == signal.SIGSTOP:
            print 'SIGSTOP'
        downloader.stop()

    if len(argv) == 4:
        downloader = Downloader(argv[1], argv[2], int(argv[3]))
    elif len(argv) == 3:
        downloader = Downloader(argv[1], argv[2], 8)
    elif len(argv) < 3:
        print "Usage: pget <url> <filename> <#connection=8>"
        return

    downloader.subscribe(download_callback, 256)

    downloader.start()

    signal.signal(signal.SIGKILL, handler)
    signal.signal(signal.SIGSTOP, handler)

    downloader.wait_for_finish()

    print "\n", downloader.total_downloaded, downloader.total_length


def main():
    if sys.stdin.isatty():
        run(sys.argv)
    else:
        argv = sys.stdin.read().split(' ')
        run(argv)
