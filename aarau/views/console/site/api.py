from pyramid.view import view_config

from aarau.views.filter import login_required
from aarau.models import (
    ReadingResult,
    Site,
)

from aarau.views.console.site.action import fetch_project


@view_config(route_name='api.console.site.application.result',
             request_method='GET',
             renderer='json')
@login_required
def api_application_site_result(req):
    """Renders result json by id."""
    project_id = req.matchdict['project_id']
    site_id = req.matchdict['id']

    project = fetch_project(project_id, req.user.id)
    try:
        Site.by_type('Application').where(
            Site.id == site_id,
            Site.project_id == project_id).get()  # pylint: disable=no-member
    except Site.DoesNotExist:  # pylint: disable=no-member
        return {'data': []}

    results = ReadingResult.fetch_data_by_path(
        project.access_key_id, site_id)
    return {'data': list(results)}
