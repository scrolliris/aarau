from pyramid.events import subscriber
from pyramid.events import BeforeRender


@subscriber(BeforeRender)
def add_carrell_renderer_globals(evt) -> None:
    """Adds global variables for carrell renderer."""
    req = evt['request']

    if req and req.subdomain == 'carrell':
        evt['cookie'] = {'carrell.sidebar': ''}
        key = 'carrell.sidebar'
        if key in req.cookies:
            evt['cookie'][key] = str(req.cookies[key])


def includeme(config):  # pylint: disable=unused-argument
    pass
