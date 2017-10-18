from pyramid.events import subscriber
from pyramid.events import BeforeRender

from aarau.env import Env


@subscriber(BeforeRender)
def set_cache_controls(event):
    request = event['request']
    env = Env()

    # disable caching
    if request and not env.is_production:
        request.response.headerlist.extend((
            ('Cache-Control', 'no-cache, no-store, must-revalidate'),
            ('Pragma', 'no-cache'),
            ('Expires', '0')
        ))
