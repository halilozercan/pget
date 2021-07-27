# Deprecated

I've abandon this project almost 3 years ago when I also stopped writing Python. Please use tools like curl, aria2, wget for file downloads over terminal.
Please consider using requests library as a Python package alternative.

# PGet

pget offers a simple yet functional API that enables you to save large files from bandwidth limited servers such as Google Drive, Yandex Disk, etc.

Basically, Downloader operates asynchronously and creates multithreads that connect to specified url from different [ranges](https://developer.mozilla.org/en-US/docs/Web/HTTP/Range_requests).

## How to get

You can install pget from PyPI using pip

```
pip install pget
```

Also you can clone this repository and install it using setuptools

```
git clone https://github.com/halilozercan/pget
cd pget
python setup.py install
```

## Usage

Pget is essentially designed to be a python module, but it also provides a nice executable to cater your download needs quickly.

```
PGet - A tool for fast downloads

positional arguments:
  http://filedownload.url/path?args=given
                        File URL
  filename.txt          File name

optional arguments:
  -h, --help            show this help message and exit
  --chunks CHUNKS, -C CHUNKS
                        Chunk count
```

This is the output of well-known argument parser of python. For example

```
pget "http://distribution.bbb3d.renderfarming.net/video/mp4/bbb_sunflower_1080p_60fps_normal.mp4" bunny.mp4 -C 8
```

In this example, we download big buck bunny video to `bunny.mp4` file from 8 different ranges.

If we want to do this in a python code

```
from pget.down import Downloader
downloader = Downloader(url, filename, chunk_count)

downloader.start()
downloader.subscribe(callback, callback_threshold)
downloader.wait_for_finish()
```

- by using subscribe, we get a callback from downloader whenever `callback_threshold` kilobytes of data is downloaded.
- start and wait_for_finish is like starting a thread and waiting to join. You can also run pget downloader in sync mod by `start_sync()`
- During the download, downloader object is updated regularly. So you can use it to get feedback in your application.
