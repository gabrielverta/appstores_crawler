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
        'name': 'Advanced Photoshop Magazine: Professional guides',
        'url': 'https://itunes.apple.com/us/app/advanced-photoshop-magazine-professional-guides/id470900017?mt=8',
    }, {
        'name': 'T.D. Jakes Ministries',
        'url': 'https://itunes.apple.com/us/app/t-d-jakes-ministries/id979567335?mt=8'
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


def test_parse_app_detail():
    """
        Test app details 
    """
    expected = dict(
      name='Kindle – Read eBooks, Magazines & Textbooks',
      icon='http://is2.mzstatic.com/image/thumb/Purple122/v4/b6/82/d1/b682d1b6-914d-da22-0b60-c48d7addf5cd/source'
           '/175x175bb.jpg',
      price=0.0,
      description='Turn your iPhone or iPad into a Kindle with the free Kindle app, and carry all your eBooks with '
                  'you, wherever you go. eBooks (including those with narration) that you have purchased on Amazon '
                  'will automatically appear in your app.  Kindle Unlimited and Amazon Prime members can select and '
                  'download eBooks directly in the app. What you’ll get:• Sample any eBook for free• Magazines, '
                  'newspapers, graphic novels and textbooks with high-res color images• A customizable reading '
                  'experience with your choice of font style, size and more• Comfortable reading day and night with '
                  'adjustable screen brightness and page color• Discover and download Kindle Unlimited eBooks and '
                  'magazines• Unique features like X-Ray, Whispersync, Page Flip, Print Replica, flashcards and more• '
                  'Instant translations and definitions, without leaving the page• Ability to make and share in-page '
                  'highlights• Bold font and text size options• Access to local library eBooks',
      developer='AMZN Mobile LLC',
      screenshots=dict(
          phone=[
        'http://a1.mzstatic.com/us/r30/Purple42/v4/8a/9c/6b/8a9c6b74-4780-8a32-f34f-f884096693f3/screen696x696.jpeg',
        'http://a2.mzstatic.com/us/r30/Purple71/v4/48/51/45/48514519-f897-d5fb-a23c-76d5c44ef9c8/screen696x696.jpeg',
        'http://a1.mzstatic.com/us/r30/Purple62/v4/00/02/6e/00026e18-b0ed-8a22-7ae4-e31aa341182d/screen696x696.jpeg',
        'http://a3.mzstatic.com/us/r30/Purple41/v4/21/bf/f8/21bff85d-b3cb-469b-9bbd-49c7f18aa629/screen696x696.jpeg',
        'http://a2.mzstatic.com/us/r30/Purple42/v4/27/d0/65/27d06586-edbd-af71-a0bb-cf365e73bda0/screen696x696.jpeg'
          ],
          tablet=[
              'http://a2.mzstatic.com/us/r30/Purple71/v4/2a/98/d7/2a98d765-0fac-ddd8-875f-53ae25fd88fe/sc1024x768.jpeg',
              'http://a1.mzstatic.com/us/r30/Purple62/v4/1b/8e/c5/1b8ec5e7-e855-c94a-7d94-128735ce80e5/sc1024x768.jpeg',
              'http://a5.mzstatic.com/us/r30/Purple62/v4/b5/e6/88/b5e688bb-abb7-9e24-cd79-5102ddee86fc/sc1024x768.jpeg',
              'http://a3.mzstatic.com/us/r30/Purple22/v4/bc/f2/22/bcf222e5-9157-0ff5-812c-d558162680f1/sc1024x768.jpeg',
              'http://a3.mzstatic.com/us/r30/Purple62/v4/0f/c6/f1/0fc6f13e-38c3-194b-ff63-ec6c736d068c/sc1024x768.jpeg'
          ]
      ),
      review=dict(
          count=167,
          value=3.96407
      )
    )

    template = open(os.path.join(TEMPLATES_PATH, "free-app.html")).read()
    kindle = apple.app(template)
    for key in expected:
        assert expected[key] == kindle[key]