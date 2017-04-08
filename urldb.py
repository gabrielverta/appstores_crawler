import settings
from aiohttp import web
from repositories import url_repository


async def list_urls(request):
    """
        GET: /api/urls
        
        :return application/json
        
            {
                "urls": ["http://url1.com", "http://url2.com"]
            }
    """
    urls = await url_repository.next_urls()
    return web.json_response({'urls': urls})


async def add_urls(request):
    """
        POST: /api/urls
        
        :return: status code 204 
    """
    data = await request.post()
    try:
        urls = data.getall('urls')
        order = data.getall('order')

        urls_to_add = [(urls[i], order[i]) for i in range(len(urls))]
        await url_repository.add_urls(urls_to_add)
    except KeyError:
        raise web.HTTPBadRequest

    raise web.HTTPNoContent


app = web.Application()
app.router.add_get('/api/urls', list_urls)
app.router.add_post('/api/urls', add_urls)

if __name__ == '__main__':
    web.run_app(app, host=settings.URLDB_HOST, port=settings.URLDB_PORT)