from pyramid.events import subscriber
from pyramid.events import BeforeRender


@subscriber(BeforeRender)
def add_console_renderer_globals(evt) -> None:
    """Adds global variables for console renderer."""
    req = evt['request']

    if req and req.subdomain == 'console':
        evt['cookie'] = {'console.sidebar': ''}
        key = 'console.sidebar'
        if key in req.cookies:
            evt['cookie'][key] = str(req.cookies[key])


def includeme(config):
    config.include('.project')
    config.include('.site')
