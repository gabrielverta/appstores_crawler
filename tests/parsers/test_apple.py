import os
from parsers import apple

TEMPLATES_PATH = os.path.join(os.path.dirname(os.path.realpath(os.path.dirname(__file__))), "templates", "apple")


def test_parse_categories():
    """
        Test that category list parser is working
         
        :return: 
    """
    shopping = {'name': 'Shopping', 'url': 'https://itunes.apple.com/us/genre/ios-shopping/id6024?mt=8'}
    template = open(os.path.join(TEMPLATES_PATH, "categories.html")).read()
    categories = apple.categories(template)
    assert 25 == len(categories)
    assert shopping['name'] in [c['name'] for c in categories]
    assert shopping['url'] in [c['url'] for c in categories if c['name'] == shopping['name']]


def test_parse_subcategories():
    """
        Test that subcategories are working
        
        :return: 
    """
    puzzle = {'name': 'Puzzle', 'url': 'https://itunes.apple.com/us/genre/ios-games-puzzle/id7012?mt=8'}
    template = open(os.path.join(TEMPLATES_PATH, "categories.html")).read()
    categories = apple.categories(template)
    names = [c['name'] for c in categories]
    assert 'Games' in names
    games = categories[names.index('Games')]
    assert 18 == len(games['children'])
    assert puzzle['name'] in [c['name'] for c in games['children']]
    assert puzzle['url'] in [c['url'] for c in games['children'] if c['name'] == puzzle['name']]