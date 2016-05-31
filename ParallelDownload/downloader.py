import sys
import tempfile
import threading

import time
import warnings

import requests

from chunk import Chunk


def readable_bytes(num, suffix='B'):
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


class Downloader:
    def __init__(self, url, file_name, chunk_count):
        self.url = url
        self.file_name = file_name
        self.chunk_count = chunk_count

        self.total_length = 0
        self.total_downloaded = 0
        self.__chunks = []

        self.last_total = 0
        self.speed = 0
        self.readable_speed = readable_bytes(self.speed)

        self.__stop = False
        self.__started = False
        self.__subs = []

        self.thread = threading.Thread(target=self.run)

    # This function registers a callback. Every second, speed thread will also update observers.
    # callable must take at least one argument. (Downloader)
    def subscribe(self, sub_callable):
        self.__subs.append(sub_callable)

    # progress: how many bytes have been downloaded.
    # number: which chunk is reporting.
    def download_callback(self, progress, number):

        self.readable_speed = readable_bytes(self.speed)
        self.total_downloaded += progress

        self.notify_subs()

        # sys.stdout.write("\rDownloading %s [%s] [%s]" %
        #                 (self.file_name, 100 * (float(self.total_downloaded) / self.total_length), readable_speed))
        # sys.stdout.flush()

    def speed_func(self):
        while not self.__stop:
            time.sleep(1)
            self.speed = self.total_downloaded - self.last_total
            self.last_total = self.total_downloaded

    def stop(self):
        for chunk in self.__chunks:
            chunk.stop()
        self.__stop = True

    def start(self):
        if self.__started:
            raise RuntimeError('Download has been already started.')

        self.thread.start()

    def wait_for_finish(self):
        self.thread.join()

    def run(self):
        self.__started = True

        r = requests.get(self.url, stream=True)
        try:
            self.total_length = int(r.headers.get('content-length'))
        except:
            self.chunk_count = 1
            warnings.warn('This url does not support parallel downloading. Normal download will continue.',
                          RuntimeWarning)

        if self.chunk_count == 1:
            chunk_file = tempfile.TemporaryFile()
            new_chunk = Chunk(self, self.url, file=chunk_file)
            self.__chunks.append(new_chunk)
            new_chunk.start()
        else:
            chunk_size = self.total_length / self.chunk_count

            for chunk_number in range(self.chunk_count):
                chunk_file = tempfile.TemporaryFile()

                if chunk_number != self.chunk_count - 1:
                    new_chunk = Chunk(self, self.url, chunk_number * chunk_size, ((chunk_number + 1) * chunk_size) - 1,
                                      chunk_file, chunk_number)
                else:
                    new_chunk = Chunk(self, self.url, chunk_number * chunk_size, self.total_length - 1,
                                      chunk_file, chunk_number)

                self.__chunks.append(new_chunk)
                new_chunk.start()

        speed_thread = threading.Thread(target=self.speed_func)
        speed_thread.start()

        for chunk in self.__chunks:
            chunk.thread.join()

        self.stop()
        speed_thread.join()

        # time to put together all parts
        with open(self.file_name, 'wb') as fout:
            for chunk in self.__chunks:
                # Go to first byte of temporary file
                chunk.file.seek(0)
                while True:
                    readbytes = chunk.file.read(1024)
                    if readbytes:
                        fout.write(readbytes)
                    else:
                        break
                chunk.file.close()

    def notify_subs(self):
        for sub in self.__subs:
            sub(self)
