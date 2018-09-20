from pyramid.httpexceptions import HTTPNotFound
from pyramid.response import Response
from pyramid.view import view_config

from aarau.views.filter import login_required
from aarau.models import Classification


@view_config(route_name='api.console.classification.tree',
             request_method='GET',
             renderer='json')
@login_required
def api_classification_tree(req):
    try:
        records = list(Classification.subtree_all())
        # subtree to options for select
        __ = req.localizer.translate
        nodes = {r.id: {
            'label': __(r.name, 'classification'),
            'value': r.notation,
            'children': []
        } for r in records}

        tree = []
        for r in records:
            node = nodes[r.id]
            if r.parent_id is None:
                tree.append(node)
            else:
                parent = nodes[r.parent_id]
                children = parent['children']
                children.append(node)
                parent['children'] = children
    except HTTPNotFound:
        return Response(status=500, json_body={
            'error': 'Internel Server Error'})

    return {'data': tree}
