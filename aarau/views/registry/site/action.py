from pyramid.view import view_config

from aarau.queries.site import get_sites
from aarau.models import (
    Site,
    Project
)
from aarau.views import tpl


@view_config(route_name='site.overview', renderer='.mako')
def site_overview(req):
    namespace = req.matchdict.get('namespace')
    slug = req.matchdict.get('slug')

    project = Project.select().where(
        Project.namespace == namespace
    ).get()

    # TODO: refactor (prefetch instance_type)
    site = Site.select(Site.instance_type).where(
        Site.project_id == project.id,
        Site.slug == slug
    ).get()

    site = get_sites(site.type, limit=1).where(
        Site.project_id == project.id,
        Site.slug == slug
    ).get()

    req.override_renderer = tpl(
        'overview.mako', resource='registry/site/{:s}'.format(site.type))
    return dict(project=project, site=site)
