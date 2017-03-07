import sys

import signal
from downloader import Downloader


def readable_bytes(num, suffix='B'):
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.1f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


def download_callback(downloader):
    sys.stdout.write("\rDownloading %s [%s%%] [%s/sec] %s %s" %
                     (downloader.file_name,
                      round(100 * (float(downloader.total_downloaded) / downloader.total_length), 2),
                      downloader.readable_speed,
                      readable_bytes(downloader.total_downloaded),
                      readable_bytes(downloader.total_length)))
    sys.stdout.flush()


def run(argv):

    def handler(signum, frame):
        if signum == signal.SIGTERM:
            print '\nTerminated'
        elif signum == signal.SIGINT:
            print '\nInterrupted'
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

    signal.signal(signal.SIGTERM, handler)
    signal.signal(signal.SIGINT, handler)

    downloader.wait_for_finish()


def main():
    if sys.stdin.isatty():
        run(sys.argv)
    else:
        argv = sys.stdin.read().split(' ')
        run(argv)
