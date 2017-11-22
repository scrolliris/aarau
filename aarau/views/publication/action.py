from pyramid.view import view_config

from aarau.models import Site
from aarau.views import tpl
from aarau.views.top import get_sites


@view_config(route_name='site.publication.view',
             renderer=tpl('publication/view.mako'))
def site_publication(req):
    site_type = 'publication'
    site = get_sites(site_type, limit=1).where(
        Site.slug == req.matchdict['slug']
    ).get()
    return dict(site_type=site_type, site=site)
