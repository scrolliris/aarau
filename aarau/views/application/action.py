from pyramid.view import view_config

from aarau.models import Site
from aarau.queries.site import get_sites
from aarau.views import tpl


@view_config(route_name='site.application.view',
             renderer=tpl('application/view.mako'))
def site_application(req):
    site_type = 'application'
    site = get_sites(site_type, limit=1).where(
        Site.hosting_id == req.matchdict['id']
    ).get()
    return dict(site_type=site_type, site=site)
