import threading
import warnings

import requests


class Chunk:
    INIT = 0
    DOWNLOADING = 1
    PAUSED = 2
    FINISHED = 3
    STOPPED = 4

    def __init__(self, downloader, url="", start_byte=-1, end_byte=-1, file="downloaded", number=-1):
        self.url = url
        self.start_byte = start_byte
        self.end_byte = end_byte
        self.file = file
        self.number = number
        self.downloader = downloader

        self.__state = Chunk.INIT

        self.progress = 0
        self.total_length = 0

    def start(self):
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def stop(self):
        self.__state = Chunk.STOPPED

    def pause(self):
        if self.__state == Chunk.DOWNLOADING:
            self.__state = Chunk.PAUSED
        else:
            warnings.warn("Cannot pause at this stage")

    def resume(self):
        if self.__state == Chunk.PAUSED:
            print self.__paused_request
            self.thread = threading.Thread(target=self.run, kwargs={'r': self.__paused_request})
            self.thread.start()
            print "chunk thread started"

    def run(self, r=None):
        self.__state = Chunk.DOWNLOADING
        if r is None:
            if self.start_byte == -1 and self.end_byte == -1:
                r = requests.get(self.url, stream=True)
            else:
                r = requests.get(self.url, stream=True,
                                 headers={"Range": "bytes=" + str(self.start_byte) + "-" + str(self.end_byte)})

                self.total_length = int(r.headers.get("content-length"))

        break_flag = False
        for part in r.iter_content(chunk_size=1024):
            self.progress += len(part)
            if part and self.__state != Chunk.STOPPED:  # filter out keep-alive new chunks
                self.file.write(part)
                self.downloader.download_callback(len(part), self)
                if self.__state == Chunk.PAUSED:
                    self.__paused_request = r
                    break_flag = True
                    break
            elif self.__state == Chunk.STOPPED:
                break_flag = True
                break

        if not break_flag:
            self.__state = Chunk.FINISHED

        self.downloader.download_callback(0, self)

    def is_finished(self):
        return self.__state == Chunk.FINISHED