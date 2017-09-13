"""User utilities
"""
from pyramid.events import subscriber
from pyramid.events import BeforeRender


@subscriber(BeforeRender)
def add_user_renderer_globals(_evt) -> None:
    """Adds global user variable for templates
    """


class UserUtil(object):
    """User utility/decorator for templates
    """
    def __init__(self, context, request, **kwargs):
        self.context, self.request = context, request
        self.__dict__.update(kwargs)
