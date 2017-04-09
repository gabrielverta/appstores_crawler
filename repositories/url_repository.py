from datetime import datetime, timedelta

import motor.motor_asyncio
import random
import settings


async def next_urls(size=10):
    """
        Returns list of urls to be crawled
        
        :param size: number of results to return 
        :return: [
            {'url': 'http://url1.com', 'categories': [{'name': 'game', 'order': 1}]}, 
            {'url': 'http://url2.com', 'categories': [{'name': 'books', 'order': -1}]}}
        ]
    """
    client = motor.motor_asyncio.AsyncIOMotorClient(settings.URLDB_MONGO['CONNECTION'])
    db = client[settings.URLDB_MONGO['DATABASE']]
    collection = db[settings.URLDB_MONGO['COLLECTION']]
    yesterday = datetime.now() - timedelta(days=1)
    results = await collection.find({'$or': [
        {'updated_at': None}, {'updated_at': {'$gt': yesterday}}
    ]}).sort([('categories.order', 1), ('updated_at', 1)]).to_list(length=size)

    await collection.update_many({'_id': {'$in': [r['_id'] for r in results]}}, {
        '$set': {'updated_at': datetime.now()}
    })

    response = []
    for result in results:
        result.pop('_id')
        try:
            result.pop('updated_at')
        except KeyError:
            pass
        response.append(result)
    return response


async def add_urls(urls_to_add):
    """
        Creates or updates urls to be add
        
        :param urls_to_add: [(url, {'name': 'game', 'order': 1}), (url, {'name': 'books', 'order': -1}), ...]  
    """
    client = motor.motor_asyncio.AsyncIOMotorClient(settings.URLDB_MONGO['CONNECTION'])
    db = client[settings.URLDB_MONGO['DATABASE']]
    collection = db[settings.URLDB_MONGO['COLLECTION']]

    for url, order in urls_to_add:
        await collection.update_one({'url': url}, {'$addToSet': {'categories': order}}, upsert=True)


async def remove_test_database():
    """
        Drop collection must be used for test purposes only 
    """
    if not settings.URLDB_MONGO['DATABASE'].startswith("test_"):
        raise Exception("You're not using a test database")

    client = motor.motor_asyncio.AsyncIOMotorClient(settings.URLDB_MONGO['CONNECTION'])
    db = client[settings.URLDB_MONGO['DATABASE']]
    collection = db[settings.URLDB_MONGO['COLLECTION']]
    await collection.drop()