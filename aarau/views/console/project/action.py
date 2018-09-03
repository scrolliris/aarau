from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound, HTTPNotFound

from aarau.views.filter import login_required
from aarau.models import (
    Membership,
    Plan,
    Project,
    Site,
    User,
)

from aarau.views.console.project import tpl
from aarau.views.console.project.form import (
    build_edit_project_form,
    build_new_project_form,
)


@view_config(route_name='console.project.overview',
             renderer=tpl('overview.mako'))
@login_required
def project_overview(req):
    """Renders a project by namespace."""
    user = req.user
    project = Project.select().join(Membership).join(User).where(
        User.id == user.id,
        Project.namespace == req.matchdict.get('namespace', '')
    ).first()
    if not project:
        raise HTTPNotFound
    sites = project.sites.order_by(Site.id.asc())
    return dict(project=project, sites=sites)


@view_config(route_name='console.project.new',
             request_method=('GET', 'POST'),
             renderer=tpl('new.mako'))
@login_required
def project_new(req):
    """Renders a form new project/Create new project."""
    user = req.user
    form = build_new_project_form(req)

    # create
    if 'submit' in req.POST:
        _ = req.translate
        if form.validate():
            with req.db.cardinal.atomic():
                project = Project(
                    name=form.name.data,
                    namespace=form.namespace.data,
                    description=form.description.data)
                project.plan = Plan.get_essential_plan()
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
            next_path = req.route_path(
                'console.project.overview', namespace=project.namespace)
            return HTTPFound(location=next_path)

        req.session.flash(_('project.creation.failure'),
                          queue='failure', allow_duplicate=False)
    return dict(form=form)


@view_config(route_name='console.project.edit',
             request_method=('GET', 'POST'),
             renderer=tpl('edit.mako'))
@login_required
def project_edit(req):
    """Renders a form for project/Update a project."""
    user = req.user
    project = Project.select().join(Membership).join(User).where(
        User.id == user.id,
        Project.namespace == req.matchdict.get('namespace', '')
    ).get()
    if not project:
        raise HTTPNotFound

    # update
    form = build_edit_project_form(req, project)
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
                'console.project.overview', namespace=project.namespace))

        req.session.flash(_('project.update.failure'),
                          queue='failure', allow_duplicate=False)
    return dict(form=form, project=project)
