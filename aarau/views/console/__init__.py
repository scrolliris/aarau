from pyramid.events import subscriber
from pyramid.events import BeforeRender


@subscriber(BeforeRender)
def add_console_renderer_globals(evt) -> None:
    """Adds global variables for console renderer."""
    req = evt.get('request')

    if req and req.subdomain == 'console':
        # sidebar (cookie)
        key = 'console.sidebar'
        evt['cookie'] = {
            key: '',
        }
        if key in req.cookies:
            evt['cookie'][key] = str(req.cookies[key])


def includeme(config):
    config.include('.classification')
    config.include('.project')
    config.include('.site')
    config.include('.article')
