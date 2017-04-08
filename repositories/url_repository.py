import motor.motor_asyncio
import settings


async def next_urls(size=10):
    client = motor.motor_asyncio.AsyncIOMotorClient(settings.URLDB_MONGO['CONNECTION'])
    db = client[settings.URLDB_MONGO['DATABASE']]
    collection = db[settings.URLDB_MONGO['COLLECTION']]
    items = await collection.find({}, {'_id': 0, 'url': 1}).to_list(length=size)
    return [i['url'] for i in items]


async def add_urls(urls_to_add):
    client = motor.motor_asyncio.AsyncIOMotorClient(settings.URLDB_MONGO['CONNECTION'])
    db = client[settings.URLDB_MONGO['DATABASE']]
    collection = db[settings.URLDB_MONGO['COLLECTION']]

    for url, order in urls_to_add:
        await collection.update_one({'url': url}, {'$set': {'order': order}}, upsert=True)


async def remove_test_database():
    if not settings.URLDB_MONGO['DATABASE'].startswith("test_"):
        raise Exception("You're not using a test database")

    client = motor.motor_asyncio.AsyncIOMotorClient(settings.URLDB_MONGO['CONNECTION'])
    db = client[settings.URLDB_MONGO['DATABASE']]
    collection = db[settings.URLDB_MONGO['COLLECTION']]
    await collection.drop()