"""The view action for top page.
"""

from pyramid.view import view_config

from aarau.views import tpl


@view_config(route_name='top', renderer=tpl('top.mako'))
def top(_request):
    """Renders top page view.
    """
    return dict()
