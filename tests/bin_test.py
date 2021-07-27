from unittest.mock import patch

from pget.bin import main


@patch("pget.bin.sys")
@patch("builtins.print")
def test_main(printer, fake_sys):
    fake_sys.argv = ['pget', 'http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4', 'BigBuckBunny.mp4', '-C', '8']
    main()