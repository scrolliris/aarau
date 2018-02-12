from pyramid.view import view_config

from aarau.views.filter import login_required


@view_config(route_name='carrell.top',
             renderer='../../templates/carrell/top.mako')
@login_required
def top(_req):
    return dict()
