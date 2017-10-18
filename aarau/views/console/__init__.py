from pyramid.events import subscriber
from pyramid.events import BeforeRender


@subscriber(BeforeRender)
def add_console_renderer_globals(_evt) -> None:
    """Adds global variables for console renderer."""
    pass


def includeme(config):
    config.include('.project')
    config.include('.site')
