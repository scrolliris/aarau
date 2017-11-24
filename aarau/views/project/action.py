from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from aarau.views.filter import login_required
from aarau.models import (
    Membership,
    Plan,
    Project,
    Site,
)

from aarau.views.project.form import build_new_project_form
from aarau.queries.site import get_sites


def get_site_type(params):
    site_type = 'publication' if (
        'type' not in params or params['type'] == 'publication'
    ) else 'application'
    return site_type


def tpl(path, resource='project'):
    return 'aarau:templates/{0:s}/{1:s}'.format(resource, path)


@view_config(route_name='project.view',
             renderer=tpl('view.mako'))
def project_view(req):
    project = Project.select().where(
        Project.namespace == req.matchdict['namespace']
    ).get()

    site_type = get_site_type(req.params)
    sites = get_sites(site_type).where(
        Site.project_id == project.id
    )

    return dict(project=project, site_type=site_type, sites=sites)


@view_config(route_name='project.new', renderer=tpl('new.mako'))
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
            next_path = req.route_url('console.project.view', id=project.id,
                                      namespace='console')
            return HTTPFound(location=next_path)
        else:
            req.session.flash(_('project.creation.failure'),
                              queue='failure', allow_duplicate=False)
    return dict(form=form)
