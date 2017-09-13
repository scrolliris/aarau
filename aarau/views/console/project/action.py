"""View actions for project.
"""
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound, HTTPNotFound

from aarau.views.filter import login_required
from aarau.models import (
    Membership,
    Plan,
    Project,
    User
)

from .form import edit_project_form, new_project_form


def tpl(path, resource='project'):
    """Return template file path.
    """
    return 'aarau:templates/console/{0:s}/{1:s}'.format(resource, path)


@view_config(route_name='console.project.view',
             renderer=tpl('view.mako'))
@login_required
def project_view(req):
    """Renders a project by id.
    """
    project_id = req.matchdict['id']
    user = req.user
    project = Project.select().join(Membership).join(User).where(
        User.id == user.id,
        Project.id == project_id
    ).get()
    if not project:
        raise HTTPNotFound
    return dict(project=project)


@view_config(route_name='console.project.new',
             request_method=('GET', 'POST'),
             renderer=tpl('new.mako'))
@login_required
def project_new(req):
    """Renders a form new project/Create new project.
    """
    user = req.user
    if len(user.projects) >= 1:  # beta
        next_path = req.route_path('console.top')
        raise HTTPFound(location=next_path)

    form = new_project_form(req)
    if 'submit' in req.POST:
        _ = req.translate
        if form.validate():
            with req.db.cardinal.atomic():
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
            next_path = req.route_path('console.project.view', id=project.id)
            return HTTPFound(location=next_path)
        else:
            req.session.flash(_('project.creation.failure'),
                              queue='error', allow_duplicate=False)
    return dict(form=form)


@view_config(route_name='console.project.edit',
             request_method=('GET', 'POST'),
             renderer=tpl('edit.mako'))
@login_required
def project_edit(req):
    """Renders a form for project/Update a project.
    """
    project_id = req.matchdict['id']
    user = req.user
    project = Project.select().join(Membership).join(User).where(
        User.id == user.id,
        Project.id == project_id
    ).get()
    if not project:
        raise HTTPNotFound
    form = edit_project_form(req, project)
    if 'submit' in req.POST:
        _ = req.translate
        if form.validate():
            project.name = form.name.data
            project.namespace = form.namespace.data
            project.plan = form.plan.data
            project.description = form.description.data
            project.save()

            req.session.flash(_('project.update.success'),
                              queue='success', allow_duplicate=False)
            return HTTPFound(location=req.route_path(
                'console.project.view', id=project.id))
        else:
            req.session.flash(_('project.update.failure'),
                              queue='error', allow_duplicate=False)
    return dict(form=form, project=project)
