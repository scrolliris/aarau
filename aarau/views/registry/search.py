from pyramid.view import view_config

from aarau.queries import PaginatedQuery
from aarau.queries.site import get_publication_sites_with_params
from aarau.views import tpl

ITEMS_PER_PAGE = 9


@view_config(route_name='registry.search',
             renderer=tpl('search_result.mako', resource='registry'))
def search(req):
    pq = None
    q = req.params.get('q', None)
    if q:
        query = get_publication_sites_with_params(q)
        pq = PaginatedQuery(query,
                            str(req.params.get('page', 1)), ITEMS_PER_PAGE)
    return dict(pq=pq)
