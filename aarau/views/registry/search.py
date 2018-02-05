from pyramid.view import view_config

from aarau.views import tpl


@view_config(route_name='search',
             renderer=tpl('search_result.mako', resource='registry'))
def search(_req):
    return dict()
