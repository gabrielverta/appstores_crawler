import itertools
from bs4 import BeautifulSoup
import urllib.parse

BASE_DOMAIN = "https://play.google.com/"


def categories(content):
    """
        Returns list of categories as follows:
            [
                {'name': 'Category', 'url': 'http://url.com', 'children': [{'name': 'sub1', 'url': 'url1'}]},
                 ...
            ]

        :param content: HTML of the page
        :return: list
    """
    response = []

    html = BeautifulSoup(content, 'html.parser')
    items = html.select('.single-title-link .title-link')

    for link in items:
        category = {'name': link.text.strip(), 'url': urllib.parse.urljoin(BASE_DOMAIN, link['href']), 'children': []}
        response.append(category)

    return response


def top_apps_from_category(content):
    """
        Returns ordered list of top apps from category as follows:
            [
                {'name': 'First App', 'url': 'http://url1.com'},
                {'name': 'Second App', 'url': 'http://url2.com'},
                 ...
            ]


        :param content: HTML of the page 
        :return: list
    """
    html = BeautifulSoup(content, 'html.parser')
    items = html.select('.card-list .card .title')

    response = []
    for item in items:
        response.append({
            'name': item['title'],
            'url': urllib.parse.urljoin(BASE_DOMAIN, item['href'])
        })

    return response


def app(content):
    """
        Map app html page to dict 

        :param content: HTML of the page
        :return: dict
    """
    html = BeautifulSoup(content, 'html.parser')
    review_count = 0
    rating_value = 0
    try:
        review_count = html.select_one('[itemprop=ratingCount]')['content']
        rating_value = html.select_one('[itemprop=ratingValue]')['content']
    except (AttributeError,):
        pass

    video = None

    video_image = html.select_one('.video-image')

    if video_image:
        video = dict(
            thumb=video_image['src'],
            url=html.select_one('.preview-overlay-container')['data-video-url']
        )
    version = ""
    try:
        version = html.select_one('[itemprop=softwareVersion]').text.strip()
    except AttributeError:
        pass

    return dict(
        name=html.select_one('.id-app-title').text,
        icon=html.select_one('[itemprop=image]')['src'],
        price=float(html.select_one('[itemprop=price]')['content'].replace("R$", "").replace("$", "").replace(",", ".")),
        description=html.select_one('[itemprop=description]').text,
        developer=html.select_one('[itemprop=author] span').text,
        screenshots=[img['src'] for img in html.select('.full-screenshot')],
        review=dict(
            count=int(review_count),
            value=float(rating_value),
            version=version
        ),
        video=video
    )


def is_url_directory(url):
    """
        Returns if an url represents an app or a directory of apps
    """
    return 'play.google.com/store/apps/details' not in url
