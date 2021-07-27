import argparse
import logging
import os
import signal
import sys

from . import down
from .log import setup_logging
from .down import Downloader

first_summary_flag = False
logger = logging.getLogger(__name__)


def download_callback(downloader):
    global first_summary_flag

    if not first_summary_flag:
        sys.stdout.write("\nDownload URL: {}\n".format(downloader.url))
        sys.stdout.write(
            "\nSaving to: {}\n".format(os.path.join(os.getcwd(), downloader.file_name)))
        sys.stdout.write("\nTotal Length: {} bytes - {}\n\n".format(
            downloader.total_length, down.readable_bytes(downloader.total_length)))
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
            done = int((downloader.total_merged * fill_in_area) / downloader.total_length) * '='
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
            logger.info('Terminated')
        elif signum == signal.SIGINT:
            logger.info('Interrupted')
        downloader.stop()

    parser = argparse.ArgumentParser(description='PGet - A tool for fast downloads')
    parser.add_argument('url', type=str, help='Download URL')
    parser.add_argument('filename', type=str, help='Saved file name')
    # parser.add_argument('--header', '-H', action='append', dest='headers')
    parser.add_argument('-C', '--chunks', dest='chunks', type=int, default=8, help='Parallel connection count')
    parser.add_argument('-F','--highspeed', dest='high_speed', default=False,
                        const=True, help='High speed connection flag', action='store_const')
    parser.add_argument('-H', '--header', dest='headers', metavar='HeaderKey: HeaderValue',
                        help='Add a HTTP Header for download connection', action='append')

    args = parser.parse_args(argv[1:])
    downloader = Downloader(args.url, args.filename, args.chunks, args.high_speed, args.headers)

    downloader.subscribe(download_callback, 256)

    downloader.start()

    signal.signal(signal.SIGTERM, handler)
    signal.signal(signal.SIGINT, handler)

    downloader.wait_for_finish()


def main():
    setup_logging(enabled=True)
    if sys.stdin.isatty():
        run(sys.argv)
    else:
        argv = sys.stdin.read().split(' ')
        run(argv)
