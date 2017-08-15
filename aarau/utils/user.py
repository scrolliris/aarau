from pyramid.events import subscriber
from pyramid.events import BeforeRender


@subscriber(BeforeRender)
def add_user_renderer_globals(evt):
    ctx, req = evt['context'], evt['request']
    return
    # user = getattr(req, 'user', None)
    # user = None
    # if user is not None:
    #     evt['user'] = req.settings['aarau.includes']['user'](
    #         ctx, req, user=user)
    # else:
    #     evt['user'] = None


class UserUtil(object):
    """
    The user utility/decorator for templates.
    """
    def __init__(self, context, request, **kwargs):
        self.context, self.request = context, request
        self.__dict__.update(kwargs)
