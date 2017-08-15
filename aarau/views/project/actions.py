"""View actions for project.
"""
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from aarau.views.filters import login_required
from aarau.models import (
    Membership,
    Plan,
    Project,
)
from .forms import new_project_form


def tpl(path, resource='project'):
    """Return template file path.
    """
    return 'aarau:templates/{0:s}/{1:s}'.format(resource, path)


@view_config(route_name='project.new', renderer=tpl('new.mako'))
@login_required
def project_new(req):
    """Renders a form new project/Create new project.
    """
    user = req.user
    if user.projects:  # beta
        next_path = req.route_path('console.top')
        raise HTTPFound(location=next_path)

    form = new_project_form(req)
    if 'submit' in req.POST:
        _ = req.translate
        if form.validate():
            with req.db.atomic():
                project = Project(
                    name=form.name.data,
                    namespace=form.namespace.data,
                    description=form.description.data)
                project.plan = Plan.get_free_plan()
                project.access_key_id = Project.grab_unique_key(
                    'access_key_id')
                project.save()
                # create membership
                user = req.user
                user.projects.add(project)
                # set membership as `primary_owner`
                membership = user.memberships.where(
                    Membership.project_id == project.id
                ).first()
                membership.role = 'primary_owner'
                membership.save()

            req.session.flash(_('project.creation.success'),
                              queue='success', allow_duplicate=False)
            next_path = req.route_url('console.project.view', id=project.id,
                                      namespace='console')
            return HTTPFound(location=next_path)
        else:
            req.session.flash(_('project.creation.failure'),
                              queue='error', allow_duplicate=False)
    return dict(form=form)
