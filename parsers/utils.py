from parsers import apple, google


def get_backend(url):
    if 'itunes.apple.com' in url:
        return apple

    return google