import urldb
import settings
from repositories import url_repository

settings.URLDB_MONGO['DATABASE'] = 'test_appstores'


def test_urldb():
    from aiohttp.test_utils import TestClient, loop_context
    app = urldb.app
    with loop_context() as loop:
        with TestClient(app, loop=loop) as client:
            async def empty_urls():
                """
                    Test GET api without results in database 
                """
                nonlocal client
                await url_repository.remove_test_database()
                response = await client.get('/api/urls')
                assert 200 == response.status
                assert 'application/json; charset=utf-8' == response.headers['content-type']
                data = await response.json()
                assert 'urls' in data
                assert 0 == len(data['urls'])

            async def add_urls():
                """
                    - Test POST to add new urls to database
                    - Test GET api to retrieve results
                """
                nonlocal client
                response = await client.post('/api/urls', data={
                    'urls': ['http://one.com', 'http://two.com', 'http://three.com'],
                    'order': [1, 2, -1],
                    'categories': ['books', 'games', 'puzzles']
                })
                assert 204 == response.status
                response = await client.get('/api/urls')
                assert 200 == response.status
                data = await response.json()
                assert 3 == len(data['urls'])
                first = data['urls'][0]

                assert 'http://one.com' == first['url']
                assert isinstance(first['categories'], list)
                assert 'books' == first['categories'][0]['name']

            loop.run_until_complete(empty_urls())
            loop.run_until_complete(add_urls())
