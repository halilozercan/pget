from __future__ import unicode_literals
from mock import patch

from pget.bin import main


@patch("pget.bin.sys")
@patch("builtins.print")
def test_main(printer, fake_sys):
    fake_sys.argv = ['pdownload', 'http://halilibo.com/filez/i/StfyyS6.mp4', 'video.mp4', '-C', '8']
    main()
