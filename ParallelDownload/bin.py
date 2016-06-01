import sys

from ParallelDownload import Downloader


def download_callback(downloader):
    sys.stdout.write("\rDownloading %s [%s] [%s] %s %s" %
                     (downloader.file_name, 100 * (float(downloader.total_downloaded) / downloader.total_length),
                      downloader.readable_speed, downloader.total_downloaded, downloader.total_length))
    sys.stdout.flush()


def run(argv):
    if len(argv) == 4:
        downloader = Downloader(argv[1], argv[2], int(argv[3]))
    elif len(argv) == 3:
        downloader = Downloader(argv[1], argv[2], 8)
    elif len(argv) < 3:
        print "Usage: pdownload <url> <filename> <chunk_count=8>"
        return

    downloader.subscribe(download_callback, 512)

    downloader.start()

    downloader.wait_for_finish()

    print "\n", downloader.total_downloaded, downloader.total_length


def main():
    if sys.stdin.isatty():
        run(sys.argv)
    else:
        argv = sys.stdin.read().split(' ')
        run(argv)
