import aiohttp
import asyncio
import settings


async def apple_categories(loop=None):
    """
        :param loop: io loop
        :return: response 
    """
    return await fetch(settings.APPLESTORE_CATEGORIES, loop)


async def ask_for_urls():
    urls_api = "http://{}:{}/api/urls".format(settings.URLDB_HOST, settings.URLDB_PORT)
    return await fetch_json(urls_api)


async def create_app(app):
    return None


async def fetch(url, loop=None):
    """
        GET HTTP request
        
        :param url: URL to fetch
        :param loop: io loop
        :return: 
    """
    loop = loop if not loop is None else asyncio.get_event_loop()
    async with aiohttp.ClientSession(loop=loop) as session:
        async with session.get(url) as response:
            return await response.text()


async def fetch_json(url, loop=None):
    """
        GET HTTP request

        :param url: URL to fetch
        :param loop: io loop
        :return: 
    """
    loop = loop if not loop is None else asyncio.get_event_loop()
    async with aiohttp.ClientSession(loop=loop) as session:
        async with session.get(url) as response:
            return await response.json()


async def post(url, loop=None, **kwargs):
    """
        POST HTTP request

        :param url: URL to fetch
        :param loop: io loop
        :return: 
    """
    loop = loop if not loop is None else asyncio.get_event_loop()
    async with aiohttp.ClientSession(loop=loop) as session:
        async with session.post(url, **kwargs) as response:
            return await response.text()


async def save_category_urls(urls):
    """
        
        :param urls: 
        :return: 
    """
    params = {
        'urls': [],
        'order': [],
        'categories': []
    }
    for url in urls:
        params['urls'].append(url['url'])
        params['order'].append(0)
        params['categories'].append(url['name'])

        for child in url['children']:
            params['urls'].append(child['url'])
            params['order'].append(0)
            params['categories'].append(child['name'])

    urls_api = "http://{}:{}/api/urls".format(settings.URLDB_HOST, settings.URLDB_PORT)
    return await post(urls_api, data=params)


async def save_directory_urls(urls):
    params = {
        'urls': [],
        'order': [],
        'categories': []
    }

    order = 1
    for url in urls:
        params['urls'].append(url['url'])
        params['order'].append(order)
        params['categories'].append(url['name'])
        order += 1

    urls_api = "http://{}:{}/api/urls".format(settings.URLDB_HOST, settings.URLDB_PORT)
    return await post(urls_api, data=params)