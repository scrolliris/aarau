from pyramid.view import view_config

from aarau.queries.site import get_sites
from aarau.views import (
    get_site_type,
    tpl
)


@view_config(route_name='top', renderer=tpl('top.mako'))
def top(req):
    site_type = get_site_type(req.params)
    sites = get_sites(site_type)

    return dict(site_type=site_type, sites=sites)
