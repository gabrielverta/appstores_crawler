import os
from parsers import apple

TEMPLATES_PATH = os.path.join(os.path.dirname(os.path.realpath(os.path.dirname(__file__))), "templates", "apple")


def test_parse_categories():
    """
        Test that category list parser is working 
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


def test_parse_top_by_category():
    """
        Test top apps inside a category
    """
    books = [{
        'name': 'Kindle – Read eBooks, Magazines & Textbooks',
        'url': 'https://itunes.apple.com/us/app/kindle-read-ebooks-magazines-textbooks/id302584613?mt=8'
    }, {
        'name': 'Audible – audio books, original series & podcasts',
        'url': 'https://itunes.apple.com/us/app/audible-audio-books-original-series-podcasts/id379693831?mt=8',
    }, {
        'name': 'Wattpad - Read unlimited books and eBooks',
        'url': 'https://itunes.apple.com/us/app/wattpad-read-unlimited-books-and-ebooks/id306310789?mt=8'
    }]
    top_count = 240

    template = open(os.path.join(TEMPLATES_PATH, "single-category.html")).read()
    top_book_apps = apple.top_apps_from_category(template)

    assert top_count == len(top_book_apps)
    for i in range(0, 3):
        expected = books[i]
        got = top_book_apps[i]
        assert expected['name'] == got['name']
        assert expected['url'] == got['url']