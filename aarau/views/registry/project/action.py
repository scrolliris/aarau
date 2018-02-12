from pyramid.view import view_config

from aarau.views import (
    get_site_type,
    tpl
)
from aarau.models import (
    Project,
    Site,
)

from aarau.queries.site import get_sites


@view_config(route_name='registry.project.overview',
             renderer=tpl('overview.mako', resource='registry/project'))
def project_overview(req):
    project = Project.select().where(
        Project.namespace == req.matchdict['namespace']
    ).get()

    site_type = get_site_type(req.params)
    sites = get_sites(site_type).where(
        Site.project_id == project.id
    )

    return dict(project=project, site_type=site_type, sites=sites)
