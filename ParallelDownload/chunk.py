import threading

import requests


class Chunk:
    def __init__(self, downloader, url="", start_byte=-1, end_byte=-1, file="downloaded", number=-1):
        self.url = url
        self.start_byte = start_byte
        self.end_byte = end_byte
        self.file = file
        self.number = number
        self.downloader = downloader

        self.__stop = False

        self.progress = 0
        self.total_length = 0
        self.thread = threading.Thread(target=self.run)

    def start(self):
        self.thread.start()

    def stop(self):
        self.__stop = True

    def run(self):
        r = requests.get(self.url, stream=True,
                         headers={"Range": "bytes=" + str(self.start_byte) + "-" + str(self.end_byte)})

        if not (self.start_byte == -1 and self.end_byte == -1):
            self.total_length = int(r.headers.get("content-length"))

        for part in r.iter_content(chunk_size=1024):
            self.progress += len(part)
            if part and not self.__stop:  # filter out keep-alive new chunks
                self.file.write(part)
                self.downloader.download_callback(len(part), self.number)
            elif self.__stop:
                break
