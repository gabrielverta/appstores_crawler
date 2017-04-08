import itertools
from bs4 import BeautifulSoup


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
    items = html.select('#genre-nav .grid3-column > .list > li')

    for item in items:
        link = item.find('a')
        category = {'name': str(link.string), 'url': link['href'], 'children': []}

        # does it have sub categories?
        if item.find('ul'):
            sub_categories = item.select('> .list > li > a')
            category['children'] = [{'name': str(c.string), 'url': c['href']} for c in sub_categories]

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
    lists = html.select('#selectedgenre #selectedcontent ul')

    response = [[], [], []]
    counter = 0
    for l in lists:
        items = l.select('li a')

        for item in items:
            response[counter].append({
                'name': str(item.string),
                'url': item['href']
            })

        counter += 1

    return list(itertools.chain.from_iterable([
        (response[0][i], response[1][i], response[2][i]) for i in range(len(response[0]))
    ]))


def app(content):
    """
    
        :param content: 
        :return: 
    """
    html = BeautifulSoup(content, 'html.parser')

    return dict(
        name=str(html.select_one('[itemprop=name]').string),
        icon=html.select_one('[itemprop=image]')['content'],
        price=float(html.select_one('[itemprop=price]')['content'].replace("$", "")),
        description=html.select_one('[itemprop=description]').text,
        developer=str(html.select_one('[itemprop=author]').string),
        screenshots=dict(
            phone=[img['src'] for img in html.select('.iphone-screen-shots [itemprop=screenshot]')],
            tablet=[img['src'] for img in html.select('.ipad-screen-shots [itemprop=screenshot]')]
        ),
        review=dict(
            count=int(html.select_one('[itemprop=reviewCount]').text.replace(" Ratings", "")),
            value=float(html.select_one('[itemprop=ratingValue]').text)
        )
    )