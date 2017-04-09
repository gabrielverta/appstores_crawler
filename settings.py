import os


APPLESTORE_CATEGORIES = "https://itunes.apple.com/us/genre/ios/id36?mt=8"

APPDB_HOST='127.0.0.1'
APPDB_PORT=9000
APPDB_MONGO = {
    'CONNECTION': 'mongodb://127.0.0.1:27017',
    'DATABASE': 'appstores',
    'COLLECTION': 'apps'
}

BASE_DIR = os.path.realpath(os.path.dirname(__file__))

URLDB_HOST='127.0.0.1'
URLDB_PORT=9001
URLDB_MONGO = {
    'CONNECTION': 'mongodb://127.0.0.1:27017',
    'DATABASE': 'appstores',
    'COLLECTION': 'urls'
}

TIME_BETWEEN_REQUESTS = [1, 5]