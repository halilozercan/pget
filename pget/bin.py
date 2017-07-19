import argparse
import os
import sys

import signal
import down
from down import Downloader

first_summary_flag = False


def download_callback(downloader):
    global first_summary_flag

    if not first_summary_flag:
        sys.stdout.write("\nDownload URL: {}\n".format(downloader.url))
        sys.stdout.write("\nSaving to: {}\n".format(os.path.join(os.getcwd(), downloader.file_name)))
        sys.stdout.write("\nTotal Length: {} bytes - {}\n\n".format(downloader.total_length,
                                                                    down.readable_bytes(downloader.total_length)))
        first_summary_flag = True

    from pget import term
    term_width, term_height = term.getTerminalSize()
    if term_width >= 100:
        term_width = 100

    if downloader.get_state() == Downloader.DOWNLOADING:
        written_update = "[{:3}%] [{}/sec]"
        percent_downloaded = int(100 * (float(downloader.total_downloaded) / downloader.total_length))
        written_update = written_update.format(
            percent_downloaded,
            downloader.readable_speed
        )

        if len(written_update) < term_width * 3 / 4:
            fill_in_area = term_width - (len(written_update) + 3)
            done = int(fill_in_area * percent_downloaded / 100) * '='
            remaining = (fill_in_area - len(done)) * ' '
            written_update += ' [{}{}]'.format(done, remaining)
        else:
            written_update += (' ' * (term_width - len(written_update)))

        if downloader.total_downloaded == downloader.total_length:
            written_update += '\n\n'

        sys.stdout.write('\r' + written_update)
        sys.stdout.flush()
    elif downloader.get_state() == Downloader.MERGING:
        written_update = "[Merging {:5}/{:5}]".format(down.readable_bytes(downloader.total_merged),
                                                      down.readable_bytes(downloader.total_length))
        if len(written_update) < term_width * 3 / 4:
            fill_in_area = term_width - (len(written_update) + 3)
            done = int((downloader.total_merged / downloader.total_length) * fill_in_area) * '='
            remaining = (fill_in_area - len(done)) * ' '
            written_update += ' [{}{}]'.format(done, remaining)
        else:
            written_update += (' ' * (term_width - len(written_update)))

        if downloader.total_merged == downloader.total_length:
            written_update += '\n\n'

        sys.stdout.write('\r' + written_update)
        sys.stdout.flush()


def run(argv):
    def handler(signum, frame):
        if signum == signal.SIGTERM:
            print '\nTerminated'
        elif signum == signal.SIGINT:
            print '\nInterrupted'
        downloader.stop()

    parser = argparse.ArgumentParser(description='PGet - A tool for fast downloads')
    parser.add_argument('url', type=str, metavar='http://filedownload.url/path?args=given', help='File URL')
    parser.add_argument('filename', type=str, metavar='filename.txt', help='File name')
    # parser.add_argument('--header', '-H', action='append', dest='headers')
    parser.add_argument('--chunks', '-C', dest='chunks', type=int, default=8, help='Chunk count')

    args = parser.parse_args(argv[1:])
    downloader = Downloader(args.url, args.filename, args.chunks)

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
