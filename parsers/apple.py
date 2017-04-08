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
    response = []

    html = BeautifulSoup(content, 'html.parser')
    items = html.select('#selectedgenre #selectedcontent ul li a')

    for item in items:
        response.append({
            'name': str(item.string),
            'url': item['href']
        })

    return response