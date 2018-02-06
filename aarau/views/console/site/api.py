from pyramid.httpexceptions import HTTPNotFound
from pyramid.response import Response
from pyramid.view import view_config

from aarau.queries import PaginatedQuery
from aarau.views.filter import login_required
from aarau.models import (
    ReadingResult,
)

from aarau.views.console.site import (
    get_project,
    get_site,
)

ITEMS_PER_PAGE = 20


@view_config(route_name='api.console.site.insights',
             request_method='GET',
             renderer='json')
@login_required
def api_application_insights(req):
    namespace = req.matchdict.get('namespace')
    slug = req.matchdict.get('slug')

    try:
        project = get_project(namespace, user=req.user)
        site = get_site(slug, project=project)
    except HTTPNotFound:
        return Response(status=404, json_body={
            'error': 'The project or site was not found'})

    q = ReadingResult.fetch_data_by_path(
        project.access_key_id, site.id)
    pq = PaginatedQuery(q, str(req.params.get('page', 1)), ITEMS_PER_PAGE)
    return {'data': list(pq.get_objects()),
            'page': pq.page,
            'page_count': pq.page_count}
