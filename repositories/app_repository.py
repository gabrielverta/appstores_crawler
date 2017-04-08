import motor.motor_asyncio
import re
import settings


async def query_app(q):
    """
        Returns list of urls to be crawled
        
        :param size: number of results to return 
        :return: [
            {'url': 'http://url1.com', 'categories': [{'name': 'game', 'order': 1}]}, 
            {'url': 'http://url2.com', 'categories': [{'name': 'books', 'order': -1}]}}
        ]
    """
    client = motor.motor_asyncio.AsyncIOMotorClient(settings.APPDB_MONGO['CONNECTION'])
    db = client[settings.APPDB_MONGO['DATABASE']]
    collection = db[settings.APPDB_MONGO['COLLECTION']]
    regex = re.compile(q, re.IGNORECASE)

    return await collection.find({'$or': [
        {'apple.url': q},
        {'google.url': q},
        {'apple.name': regex},
        {'google.name': regex}
    ]}, {'_id': 0}).to_list(length=10)


async def add_app(app):
    """
        Creates or updates urls to be add
        
        :param urls_to_add: [(url, {'name': 'game', 'order': 1}), (url, {'name': 'books', 'order': -1}), ...]  
    """
    if not 'apple' in app and not 'google' in app:
        raise KeyError("Invalid app")

    if 'apple' in app and (
            not 'url' in app['apple']
                    or not 'name' in app['apple']
                or not app['apple']['name']
            or not app['apple']['url']
    ):
        raise KeyError("Invalid app")

    if 'google' in app and (
                        not 'url' in app['google']
                    or not 'name' in app['google']
                or not app['google']['name']
            or not app['google']['url']
    ):
        raise KeyError("Invalid app")

    client = motor.motor_asyncio.AsyncIOMotorClient(settings.APPDB_MONGO['CONNECTION'])
    db = client[settings.APPDB_MONGO['DATABASE']]
    collection = db[settings.APPDB_MONGO['COLLECTION']]

    if 'apple' in app:
        await collection.replace_one({'apple.url': app['apple']['url']}, app, upsert=True)

    if 'google' in app:
        await collection.replace_one({'google.url': app['google']['url']}, app, upsert=True)


async def remove_test_database():
    """
        Drop collection must be used for test purposes only 
    """
    if not settings.APPDB_MONGO['DATABASE'].startswith("test_"):
        raise Exception("You're not using a test database")

    client = motor.motor_asyncio.AsyncIOMotorClient(settings.APPDB_MONGO['CONNECTION'])
    db = client[settings.APPDB_MONGO['DATABASE']]
    collection = db[settings.APPDB_MONGO['COLLECTION']]
    await collection.drop()