from pget import Downloader


def sha1sum(file_name):
    import hashlib
    BUF_SIZE = 65536

    sha1 = hashlib.sha1()

    with open(file_name, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            sha1.update(data)

    return sha1.hexdigest()


Downloader(
    'http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4',
    'BigBuckBunny.mp4',
    8
).start_sync()

assert sha1sum('BigBuckBunny.mp4') == 'b29ae9b33d33304b3b966f2921cc5bfb3cb3c3ce'
