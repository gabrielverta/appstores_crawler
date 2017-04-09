import os
import re
from parsers import apple

SPACELESS = re.compile(r'\s', re.MULTILINE)
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
        screenshots=dict(phone=[
           'http://a1.mzstatic.com/us/r30/Purple42/v4/8a/9c/6b/8a9c6b74-4780-8a32-f34f-f884096693f3/screen696x696.jpeg',
           'http://a2.mzstatic.com/us/r30/Purple71/v4/48/51/45/48514519-f897-d5fb-a23c-76d5c44ef9c8/screen696x696.jpeg',
           'http://a1.mzstatic.com/us/r30/Purple62/v4/00/02/6e/00026e18-b0ed-8a22-7ae4-e31aa341182d/screen696x696.jpeg',
           'http://a3.mzstatic.com/us/r30/Purple41/v4/21/bf/f8/21bff85d-b3cb-469b-9bbd-49c7f18aa629/screen696x696.jpeg',
           'http://a2.mzstatic.com/us/r30/Purple42/v4/27/d0/65/27d06586-edbd-af71-a0bb-cf365e73bda0/screen696x696.jpeg'
        ], tablet=[
           'http://a2.mzstatic.com/us/r30/Purple71/v4/2a/98/d7/2a98d765-0fac-ddd8-875f-53ae25fd88fe/sc1024x768.jpeg',
           'http://a1.mzstatic.com/us/r30/Purple62/v4/1b/8e/c5/1b8ec5e7-e855-c94a-7d94-128735ce80e5/sc1024x768.jpeg',
           'http://a5.mzstatic.com/us/r30/Purple62/v4/b5/e6/88/b5e688bb-abb7-9e24-cd79-5102ddee86fc/sc1024x768.jpeg',
           'http://a3.mzstatic.com/us/r30/Purple22/v4/bc/f2/22/bcf222e5-9157-0ff5-812c-d558162680f1/sc1024x768.jpeg',
           'http://a3.mzstatic.com/us/r30/Purple62/v4/0f/c6/f1/0fc6f13e-38c3-194b-ff63-ec6c736d068c/sc1024x768.jpeg'
        ]),
        review=dict(
            count=167,
            value=3.96407,
            version='5.9.1'
        )
    )

    template = open(os.path.join(TEMPLATES_PATH, "free-app.html")).read()
    kindle = apple.app(template)
    for key in expected:
        assert expected[key] == kindle[key]


def test_parse_paid_app_detail():
    """
        Test paid app details 
    """
    expected = dict(
        name='Facetune',
        icon='http://is5.mzstatic.com/image/thumb/Purple122/v4/80/e1/a1/80e1a19a-cbe2-91e8-2c63-428bbd296d60/source'
             '/175x175bb.jpg',
        price=3.99,
        description="""Facetune 2 is now available on the App Store!\n\n• "Facetune helps you look your Hollywood 
        best, even in photos taken on mobile phones." - Roy Furchgott, The NY Times\n• Facetune is a fun and powerful 
        portrait & selfie photo editor!\n• #1 Photo and Video App in 127 
        countries!\n\n---------------------------------------------------------\n\nProfessional photographers and 
        graphic designers constantly photoshop models to perfection, and now so can you! Without the expensive price 
        tag or complicated tools, Facetune gives you the ability to retouch and add artistic flair to selfies and 
        portraits with ease, from the convenience of your iPhone.\n\nPraises about Facetune:\n• "Facetune helps you 
        look your Hollywood best, even in photos taken on mobile phones." - Roy Furchgott, The NY Times\n• "One of 
        the Most Powerful Mobile Apps I have Ever Encountered... Facetune Can Truly Be Called Magical." - Hillel 
        Fuld, Huffington Post\n• “I have been seriously impressed with the patch quality FaceTune does. You get 
        pretty much a Photoshop editing job in the palm of your hand.” - Allyson Kazmucha, 
        iMore\n\n---------------------------------------------------------\n\nEvery photo could use a touch up. 
        That's why magazines use expensive and complicated tools like Photoshop to make people look their best. But 
        now, there’s Facetune! Facetune provides easy-to-use, powerful tools (previously reserved only for the pros) 
        to perfect every photo or selfie, making each one look like it came straight out of a high-fashion magazine. 
        Now you can be sure that all your portraits show only the best version of you - whether you’ll be using them 
        for your professional profile or simply sharing online with 
        friends.\n\n---------------------------------------------------------\n\nWhat can Facetune do for 
        you?\n\nPERFECT SMILES\n• Widen or refine your smile\n• Whiten and brighten your teeth\n\nBEAUTIFUL SKIN\n• 
        Smooth and rejuvenate your skin\n• Remove temporary imperfections like pimples and blemishes\n• Brighten dark 
        circles under your eyes\n\nPENETRATING EYES\n• Emphasize your eyes for a penetrating gaze\n• Change your eye 
        color\n• Remove red and white-eye effects\n\nHAIR SALON\n• Color over grey hair\n• Fill bald patches\n• 
        Remove stray hairs\n\nRESHAPE FACIAL STRUCTURE\n• Refine jaw lines\n• Heighten cheek bones and brows\n• 
        Reshape your nose\n• Enlarge or shrink a specific area of the image\n• Totally transform your face into alien 
        or other fun shapes\n\nVIVID MAKEUP\n• Apply any shade of blush and eye shadow\n• Add volume to your lashes 
        and shape your brows\n• Add color to your lips\n• Add intensity to your natural lip color\n\nPHOTO 
        ENHANCEMENTS\n• Focus the photo on you, by defocusing or blurring the background\n• Improve lighting or add 
        special effects\n• Create customized filters\n• Add unique textures and customizable frames\n• Rotate the 
        photo or flip to its mirror image\n\nMAKE ART\n• Add artistic touches to make your photo your own\n• 
        Customizable filters can be applied to the entire photo or to specific areas\n\nSHOW OFF\n• Instantly share 
        your edited photos with your friends & family through social media or e-mail\n\nEASY AND FUN\n• Compare your 
        work with the original photo at every step of the way, with only one tap\n• Having trouble? Facetune offers 
        informative graphic and video help screens for each feature\n\nRESOLUTIONS\n• iPhone 6S, 6S Plus: 12.6 MP\n• 
        iPhone 6, 6 Plus 16.8 MP\n• iPhone 5, 5C, 5S: 12.6 MP\n• iPhone 4S: 8 MP\n• iPhone 4: 4.1 MP""",
        developer='Lightricks Ltd.',
        screenshots=dict(phone=[
            'http://a5.mzstatic.com/us/r30/Purple4/v4/ac/29/9e/ac299e60-01eb-dcbc-575b-c5a8c2070a72/screen696x696.jpeg',
            'http://a3.mzstatic.com/us/r30/Purple4/v4/87/0d/e1/870de137-3646-b0b6-7af4-3fa4c7999f39/screen696x696.jpeg',
            'http://a2.mzstatic.com/us/r30/Purple4/v4/4b/77/79/4b77799b-d298-807d-a02f-cfa962f18350/screen696x696.jpeg',
            'http://a3.mzstatic.com/us/r30/Purple4/v4/bb/eb/a9/bbeba9b5-b42e-f5a2-8b77-afcef7bbb7c7/screen696x696.jpeg',
            'http://a4.mzstatic.com/us/r30/Purple3/v4/0d/ef/8d/0def8d61-eddf-8a7b-0ea9-caa3af46f1b6/screen696x696.jpeg'
        ], tablet=[]),
        review=dict(
            count=33,
            value=3.84848,
            version='2.6.3'
        )
    )

    template = open(os.path.join(TEMPLATES_PATH, "paid-app.html")).read()
    kindle = apple.app(template)
    for key in expected:
        if key == 'description': # no way to make this string comparison using spaces
            assert SPACELESS.sub('', expected[key]) == SPACELESS.sub('', kindle[key])
            continue
        assert expected[key] == kindle[key]


def test_is_url_directory():
    """
        Test function that verifies if the URL is a directory or an app 
    """
    kindle_ios = "https://itunes.apple.com/us/app/kindle-read-ebooks-magazines-textbooks/id302584613?mt=8"
    ios_books = "https://itunes.apple.com/us/genre/ios-books/id6018?mt=8"
    assert not apple.is_url_directory(kindle_ios)
    assert apple.is_url_directory(ios_books)