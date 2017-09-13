from pyramid.view import view_config

from aarau.views.filter import login_required


@view_config(route_name='console.top',
             renderer='../../templates/console/top.mako')
@login_required
def top(req):
    user = req.user
    return dict(projects=user.projects)
