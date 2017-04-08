from urllib.parse import urlencode

import appdb
import settings
from repositories import app_repository

settings.APPDB_MONGO['DATABASE'] = 'test_appstores'


def app_for_testing():
    return dict(
        apple=dict(
            name='Kindle – Read eBooks, Magazines & Textbooks',
            icon='http://is2.mzstatic.com/image/thumb/Purple122/v4/b6/82/d1/b682d1b6-914d-da22-0b60-c48d7addf5cd/source'
                 '/175x175bb.jpg',
            developer='AMZN Mobile LLC',
            price=0.0,
            description='Apple description',
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
    ),
            url='https://itunes.apple.com/us/app/kindle-read-ebooks-magazines-textbooks/id302584613?mt=8'
        ), google=dict(
            url='https://play.google.com/store/apps/details?id=com.amazon.kindle',
            name='Amazon Kindle',
            icon='https://lh5.ggpht.com/sxnFjIWmIPhBg09VXkKdVY-Rwn7l1Bfxq-eo6wIM1d2wWHDApGk3w-3NN77Td_BwYz4=w300',
            developer='Amazon Mobile LLC',
            price=0.0,
            description='Google description',
            video=dict(
                thumb='//i.ytimg.com/vi/rOhhw1hn6-c/hqdefault.jpg',
                url='https://www.youtube.com/embed/rOhhw1hn6-c?ps=play&vq=large&rel=0&autohide=1&showinfo=0&autoplay'
                    '=1&authuser=0 '
            ),
    screenshots=[
        'https://lh3.googleusercontent.com/Kqcd9lmU827lmcLMqQNE1dYsldvIHPE7lf-u_i5HeUlmRVc59tMS8mCKZj0ZpZUDH-k=h310',
        'https://lh3.googleusercontent.com/SdMhZR1RkqbIQADmfeCAi3REsBEG83cjxZ4W6QxYq4L2YwhzcgUfQOAZVSviJkK5nHI=h900',
        'https://lh3.googleusercontent.com/aOojv6VRCA7k17ku-0lE9k5RJHcIubWFeaEH0qMkNVCEV4sR0I8xaMRR3QRvZu2QpA=h900'
    ]),
    review=dict(
        count=681914,
        value=4.149043560028076,
        numDownloads='100,000,000 - 500,000,000'
    ))


def test_appdb():
    from aiohttp.test_utils import TestClient, loop_context
    app = appdb.app
    with loop_context() as loop:
        with TestClient(app, loop=loop) as client:
            async def without_query():
                """
                    Test GET api without query parameter 
                """
                nonlocal client
                response = await client.get('/api/apps')
                assert 400 == response.status

            async def empty_apps():
                """
                    Test GET api without results in database
                """
                nonlocal client
                await app_repository.remove_test_database()
                url = "https://itunes.apple.com/us/app/kindle-read-ebooks-magazines-textbooks/id302584613?mt=8"
                response = await client.get('/api/apps?q={}'.format(url))
                assert 200 == response.status
                assert 'application/json; charset=utf-8' == response.headers['content-type']
                data = await response.json()
                assert 'apps' in data
                assert 0 == len(data['apps'])

            async def query_by_url():
                """
                    Test GET api filtering results by URL
                """
                nonlocal client
                await app_repository.remove_test_database()
                await app_repository.add_app(app_for_testing())
                url = "https://itunes.apple.com/us/app/kindle-read-ebooks-magazines-textbooks/id302584613?mt=8"
                response = await client.get('/api/apps?q={}'.format(url))
                assert 200 == response.status
                assert 'application/json; charset=utf-8' == response.headers['content-type']
                data = await response.json()
                assert 'apps' in data
                assert 1 == len(data['apps'])
                assert "Kindle – Read eBooks, Magazines & Textbooks" == data['apps'][0]['apple']['name']

            async def query_by_name():
                """
                    Test GET api filtering results by Name
                """
                nonlocal client
                await app_repository.remove_test_database()
                await app_repository.add_app(app_for_testing())
                name = "kindle"
                response = await client.get('/api/apps?q={}'.format(name))
                assert 200 == response.status
                assert 'application/json; charset=utf-8' == response.headers['content-type']
                data = await response.json()
                assert 'apps' in data
                assert 1 == len(data['apps'])
                assert "Kindle – Read eBooks, Magazines & Textbooks" == data['apps'][0]['apple']['name']

            async def add_app():
                """
                    - Test POST to add new app to database
                    - Test GET api to retrieve result
                """
                nonlocal client
                testing = 'testing'
                app_to_add = app_for_testing()
                del app_to_add['apple']
                app_to_add['google']['name'] = testing
                response = await client.post('/api/apps', json=app_to_add)
                assert 204 == response.status
                response = await client.get('/api/apps?q=testing')
                assert 200 == response.status
                data = await response.json()
                assert 1 == len(data['apps'])
                first = data['apps'][0]

                assert testing == first['google']['name']

            async def add_app_without_name():
                """
                    - Test POST to add new app without name
                """
                nonlocal client
                testing = 'testing'
                app_to_add = app_for_testing()
                del app_to_add['apple']
                app_to_add['google']['name'] = ''
                response = await client.post('/api/apps', json=app_to_add)
                assert 400 == response.status

            loop.run_until_complete(without_query())
            loop.run_until_complete(empty_apps())
            loop.run_until_complete(query_by_url())
            loop.run_until_complete(query_by_name())
            loop.run_until_complete(add_app())
            loop.run_until_complete(add_app_without_name())
