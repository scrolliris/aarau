import math

from pyramid.decorator import reify
from pyramid.view import view_config

from aarau.views.filter import login_required
from aarau.models import (
    ReadingResult,
    Site,
)

from aarau.views.console.site.action import fetch_project

ITEMS_PER_PAGE = 2


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


@view_config(route_name='api.console.site.application.result',
             request_method='GET',
             renderer='json')
@login_required
def api_application_site_result(req):
    """Renders result json by id."""
    project_id = req.matchdict.get('project_id')
    site_id = req.matchdict.get('id')

    project = fetch_project(project_id, req.user.id)
    try:
        Site.by_type('Application').where(
            Site.id == site_id,
            Site.project_id == project_id).get()  # pylint: disable=no-member
    except Site.DoesNotExist:  # pylint: disable=no-member
        return {'data': []}

    q = ReadingResult.fetch_data_by_path(
        project.access_key_id, site_id)
    pq = PaginatedQuery(q, str(req.params.get('page', 1)), ITEMS_PER_PAGE)
    return {'data': list(pq.get_objects()),
            'page': pq.page,
            'page_count': pq.page_count}
