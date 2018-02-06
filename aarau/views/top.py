from pyramid.view import view_config

from aarau.views import tpl
from aarau.views.console.project.form import build_new_project_form


@view_config(route_name='top', renderer=tpl('top.mako'))
def top(req):
    form = build_new_project_form(req)
    return dict(form=form)
