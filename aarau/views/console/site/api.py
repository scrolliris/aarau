from pyramid.httpexceptions import HTTPNotFound
from pyramid.response import Response
from pyramid.view import view_config

from aarau.models import ReadingResult
from aarau.queries import PaginatedQuery
from aarau.queries.project import get_project
from aarau.queries.site import get_site
from aarau.views.filter import login_required

ITEMS_PER_PAGE = 20


@view_config(route_name='console.api.site.insights.data',
             request_method='GET',
             renderer='json')
@login_required
def api_application_insights_data(req):
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


@view_config(route_name='console.api.site.insights.metrics',
             request_method='GET',
             renderer='json')
@login_required
def api_application_insights_metrics(req):
    namespace = req.matchdict.get('namespace')
    slug = req.matchdict.get('slug')

    try:
        project = get_project(namespace, user=req.user)
        _ = get_site(slug, project=project)
    except HTTPNotFound:
        return Response(status=404, json_body={
            'error': 'The project or site was not found'})

    # TODO
    # dummy
    data = [
        {'duration': 20, 'rate': 3, 'date': '20180631102324'},
        {'duration': 123, 'rate': 10, 'date': '20180631113032'},
        {'duration': 11, 'rate': 4, 'date': '20180631113500'},
        {'duration': 222, 'rate': 18, 'date': '20180631122412'},
        {'duration': 150, 'rate': 11, 'date': '20180701001239'},
        {'duration': 556, 'rate': 33, 'date': '20180701114134'},
        {'duration': 25, 'rate': 3, 'date': '20180702113134'},
        {'duration': 15, 'rate': 2, 'date': '20180702133134'},
        {'duration': 33, 'rate': 9, 'date': '20180702143134'},
        {'duration': 123, 'rate': 11, 'date': '20180702143134'},
        {'duration': 150, 'rate': 18, 'date': '20180703143134'},
        {'duration': 9, 'rate': 1, 'date': '20180703153134'},
        {'duration': 38, 'rate': 5, 'date': '20180703113134'},
        {'duration': 800, 'rate': 90, 'date': '20180704113134'},
        {'duration': 700, 'rate': 60, 'date': '20180704222124'},
        {'duration': 120, 'rate': 15, 'date': '20180704232124'},
        {'duration': 411, 'rate': 30, 'date': '20180704242124'},
        {'duration': 800, 'rate': 66, 'date': '20180704243124'},
        {'duration': 180, 'rate': 20, 'date': '20180704243124'},
        {'duration': 105, 'rate': 18, 'date': '20180635102334'},
        {'duration': 605, 'rate': 67, 'date': '20180704113134'},
        {'duration': 405, 'rate': 20, 'date': '20180636102334'},
        {'duration': 12, 'rate': 2, 'date': '20180704113134'},
        {'duration': 24, 'rate': 9, 'date': '20180704113134'},
        {'duration': 11, 'rate': 1, 'date': '20180704113134'},
        {'duration': 19, 'rate': 3, 'date': '20180704113134'},
        {'duration': 4, 'rate': 2, 'date': '20180704113134'},
        {'duration': 3, 'rate': 1, 'date': '20180637102334'},
        {'duration': 5, 'rate': 1, 'date': '20180638102334'},
        {'duration': 2, 'rate': 1, 'date': '20180639102334'},
    ]

    return {'data': data}
