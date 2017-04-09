from parsers import utils


def test_get_backend():
    """
        Test returning backend depending on URL 
    """
    kindle_ios = "https://itunes.apple.com/us/app/kindle-read-ebooks-magazines-textbooks/id302584613?mt=8"
    kindle_android = "https://play.google.com/store/apps/details?id=com.amazon.kindle"
    assert utils.apple == utils.get_backend(kindle_ios)
    assert utils.google == utils.get_backend(kindle_android)