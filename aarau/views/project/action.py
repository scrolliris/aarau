from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from aarau.views import tpl
from aarau.views.filter import login_required
from aarau.models import (
    Membership,
    Plan,
    Project,
)

from aarau.views.project.form import build_new_project_form


@view_config(route_name='project.new',
             renderer=tpl('new.mako', resource='project'))
@login_required
def project_new(req):
    """Renders a form new project/Create new project."""
    user = req.user
    if user.projects:  # beta
        next_path = req.route_path('console.top')
        raise HTTPFound(location=next_path)

    form = build_new_project_form(req)
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
            next_path = req.route_url(
                'console.project.overview', namespace=project.namspace)
            return HTTPFound(location=next_path)
        else:
            req.session.flash(_('project.creation.failure'),
                              queue='failure', allow_duplicate=False)
    return dict(form=form)
