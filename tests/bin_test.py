from mock import patch

from ParallelDownload.bin import main


@patch("ParallelDownload.bin.sys")
@patch("__builtin__.print")
def test_main(printer, fake_sys):
    fake_sys.argv = ['pdownload', "http://halilibo.com/filez/i/oqwJ2Sx.gif", "dealwithit.gif", 4]
    main()