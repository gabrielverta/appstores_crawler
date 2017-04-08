import settings
from aiohttp import web
from repositories import app_repository


async def list_apps(request):
    """
        GET: /api/urls

        :return application/json

            {
                "urls": ["http://url1.com", "http://url2.com"]
            }
    """
    try:
        apps = await app_repository.query_app(request.query['q'])
    except KeyError:
        raise web.HTTPBadRequest

    return web.json_response({'apps': apps})


async def add_app(request):
    data = await request.json()
    try:
        await app_repository.add_app(data)
    except KeyError:
        raise web.HTTPBadRequest

    raise web.HTTPNoContent

app = web.Application()
app.router.add_get('/api/apps', list_apps)
app.router.add_post('/api/apps', add_app)

if __name__ == '__main__':
    web.run_app(app, host=settings.APPDB_HOST, port=settings.APPDB_PORT)