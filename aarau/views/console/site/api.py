import math

from pyramid.decorator import reify
from pyramid.httpexceptions import HTTPNotFound
from pyramid.response import Response
from pyramid.view import view_config

from aarau.views.filter import login_required
from aarau.models import (
    ReadingResult,
)

from aarau.views.console.site import (
    get_project,
    get_site,
)

ITEMS_PER_PAGE = 20


class PaginatedQuery:
    def __init__(self, query_or_model, current_page, items_per_page):
        self._current_page = current_page
        self._items_per_page = items_per_page
        self._query = query_or_model

    @reify
    def page(self):
        if self._current_page and self._current_page.isdigit():
            return max(1, int(self._current_page))
        return 1

    @reify
    def page_count(self):
        return int(math.ceil(
            float(self._query.count()) / self._items_per_page))

    def get_objects(self):
        if self.page > self.page_count:
            return ()
        return self._query.paginate(self.page, self._items_per_page)


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
