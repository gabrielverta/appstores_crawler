import asyncio
import datetime
import logging
import os

import aiohttp

import settings
import time
from parsers import apple, google, utils
from random import randint
from repositories import crawler_repository as repository


logging.basicConfig(
    level=logging.DEBUG,
    filemode='a',
    filename=os.path.join(settings.BASE_DIR, "logs", "{}.log".format(datetime.date.today())),
    format='%(asctime)s - %(levelname)s - %(message)s',
)


async def categories():
    """
        Directory of categories to start 
    """
    logging.debug("Downloading apple categories")
    content = await repository.apple_categories()
    urls = apple.categories(content)
    logging.debug("Saving apple categories")
    await repository.save_category_urls(urls)
    logging.debug("Downloading google categories")
    google_content = await repository.google_categories()
    google_urls = google.categories(google_content)
    logging.debug("Saving google categories")
    await repository.save_category_urls(google_urls)


async def crawler():
    """
        The crawler itself:
         - ask for urls
         - fetch content
         - in case of directory: save urls from directory (category)
         - otherwise it is an app to be saved
    """
    urls = await repository.ask_for_urls()
    logging.debug("{} urls returned".format(len(urls['urls'])))
    for url in urls['urls']:
        uri = url['url']
        logging.debug("fetching url {}".format(uri))
        try:
            content = await repository.fetch(uri)
        except aiohttp.client_exceptions.ClientPayloadError:
            logging.error("Could not download {}".format(uri))
            timer = settings.TIME_BETWEEN_REQUESTS
            wait = randint(timer[0], timer[1])
            await repository.readd(url)
            logging.info("Waiting {} seconds to try again".format(wait))
            time.sleep(wait)

        backend = utils.get_backend(uri)
        logging.debug("{} backend: {}".format(backend.__name__, uri))
        if backend.is_url_directory(uri):
            apps = backend.top_apps_from_category(content)
            logging.debug("{} apps found".format(len(apps)))
            await repository.save_directory_urls(apps, url['categories'])
        else:
            app = backend.app(content)
            logging.debug("{} app will be created".format(app['name']))
            await repository.create_app(backend, url, app)


def run():
    """
        Run crawler forever 
    """
    logging.info("Starting crawler")
    timer = settings.TIME_BETWEEN_REQUESTS
    loop = asyncio.get_event_loop()
    loop.run_until_complete(categories())
    while True:
        try:
            loop.run_until_complete(crawler())
            wait = randint(timer[0], timer[1])
            logging.info("Waiting {} seconds".format(wait))
            time.sleep(wait)
        except KeyboardInterrupt:
            break

    logging.info("Stopping crawler")
    try:
        loop.close()
    except RuntimeError:
        pass


if __name__ == '__main__':
    run()