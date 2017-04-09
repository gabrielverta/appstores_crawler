import aiohttp
import asyncio
import settings
from parsers import utils


async def apple_categories(loop=None):
    """
        Fetch URL of the directory of categories
    
        :param loop: io loop
        :return: html of the page 
    """
    return await fetch(settings.APPLESTORE_CATEGORIES, loop)


async def google_categories(loop=None):
    return await fetch(settings.GOOGLESTORE_CATEGORIES, loop)


async def ask_for_urls():
    """
        Calls urldb to get next pool of URLs
    
        :return: {'urls': []} 
    """
    urls_api = "http://{}:{}/api/urls".format(settings.URLDB_HOST, settings.URLDB_PORT)
    return await fetch_json(urls_api)


async def create_app(backend, url, app):
    """
        Creates an app
        
        :param backend: 
        :param url: 
        :param app: 
        :return: 
    """
    document = {}
    store = 'apple'
    if backend == utils.google:
        store = 'google'

    document[store] = app
    document[store]['url'] = url['url']
    document[store]['ranking'] = url['categories']

    apps_api = "http://{}:{}/api/apps".format(settings.APPDB_HOST, settings.APPDB_PORT)
    return await post(apps_api, None, json=document)


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
        Save URLs that came from directory of categories
        
        :param urls: 
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


async def save_directory_urls(urls, categories):
    """
        Save URLs that came from the page of a category
    
        :param urls:  
        :param categories
    """
    params = {
        'urls': [],
        'order': [],
        'categories': []
    }

    order = 1
    for url in urls:
        params['urls'].append(url['url'])
        params['order'].append(order)
        params['categories'].append(categories[0]['name'])
        order += 1

    urls_api = "http://{}:{}/api/urls".format(settings.URLDB_HOST, settings.URLDB_PORT)
    return await post(urls_api, data=params)


async def readd(url):
    order = -1
    category = ''

    if 'categories' in url and url['categories']:
        order = url['categories'][0]['order']
        category = url['categories'][0]['name']

    params = {
        'urls': [url['url']],
        'order': [order],
        'categories': [category]
    }

    urls_api = "http://{}:{}/api/urls".format(settings.URLDB_HOST, settings.URLDB_PORT)
    return await post(urls_api, data=params)