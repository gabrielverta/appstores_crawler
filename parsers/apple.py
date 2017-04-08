from bs4 import BeautifulSoup


def categories(content):
    """
        Returns list of categories as follows:
            [
                {'name': 'Category', 'url': 'http://url.com', 'children': [{'name': 'sub1', 'url': 'url1'}] 
            ]
        
        :param content: HTML of the page 
        :return: list
    """
    html = BeautifulSoup(content, 'html.parser')
    nav = html.select("#genre-nav .grid3-column")[0]
    items = nav.select('> .list > li')

    response = []
    for item in items:
        link = item.find('a')
        category = {'name': str(link.string), 'url': link['href'], 'children': []}

        if item.find('ul'):
            sub_categories = item.select('> .list > li > a')
            category['children'] = [{'name': str(c.string), 'url': c['href']} for c in sub_categories]

        response.append(category)

    return response
