from pyramid.events import subscriber
from pyramid.events import BeforeRender


@subscriber(BeforeRender)
def add_console_renderer_globals(evt):
    req = evt['request']
    pass


def includeme(config):
    """
    Initializes console view.
    """

    config.include('.project')
    config.include('.site')
