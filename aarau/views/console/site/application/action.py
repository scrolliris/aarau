from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound, HTTPNotFound

from aarau.views.filter import login_required
from aarau.models import (
    Application,
    Site,
)
from aarau.services.interface import IReplicator

from aarau.views.console.site import fetch_project, tpl
from aarau.views.console.site.form import (
    build_edit_application_site_form,
    build_new_application_site_form,
)


@view_config(route_name='console.site.application.new',
             renderer=tpl('new.mako', type_='application'))
@login_required
def application_site_new(req):
    """Renders a form or save new application site."""
    # TODO: Use predicate
    if 'type' not in req.params or req.params['type'] != 'application':
        raise HTTPNotFound

    project = fetch_project(req.matchdict.get('project_id'), req.user.id)
    site = Site(
        project=project,
        hosting_type='Application',
        calculation_state='off',
    )
    form = build_new_application_site_form(req)
    if 'submit' in req.POST:
        _ = req.translate
        if form.validate():
            with req.db.cardinal.atomic():
                application = Application(
                    name=form.application.form.name.data,
                    description=form.application.form.description.data)
                application.save()

                site.hosting_id = application.id
                site.domain = form.domain.data
                site.read_key = Site.grab_unique_key('read_key')
                site.write_key = Site.grab_unique_key('write_key')
                site.save()

            replicator = req.find_service(iface=IReplicator, name='site')
            replicator.assign(obj=site)
            replicator.replicate()

            req.session.flash(_('site.application.creation.success'),
                              queue='success', allow_duplicate=False)
            next_path = req.route_path('console.project.view', id=project.id)
            return HTTPFound(location=next_path)
        else:
            req.session.flash(_('site.application.creation.failure'),
                              queue='failure', allow_duplicate=False)

    return dict(form=form, project=project, site=site)


@view_config(route_name='console.site.application.edit',
             renderer=tpl('edit.mako', type_='application'))
@login_required
def application_site_edit(req):
    """Renders a form for site to update."""
    if 'type' not in req.params or req.params['type'] != 'application':
        raise HTTPNotFound

    project_id = req.matchdict.get('project_id')
    site_id = req.matchdict.get('id')

    project = fetch_project(project_id, req.user.id)
    site = Site.by_type(req.params['type']).where(
        Site.id == site_id,
        Site.project_id == project_id).get()  # pylint: disable=no-member

    form = build_edit_application_site_form(req, site)
    if 'submit' in req.POST:
        _ = req.translate
        if form.validate():
            with req.db.cardinal.atomic():
                site.application.name = form.application.form.name.data
                site.application.description = \
                    form.application.form.description.data
                site.application.save()

                site.domain = form.domain.data
                site.save()

            replicator = req.find_service(iface=IReplicator, name='site')
            replicator.assign(obj=site)
            replicator.replicate()

            req.session.flash(_('site.application.update.success'),
                              queue='success', allow_duplicate=False)
            next_path = req.route_path('console.project.view', id=project.id)
            return HTTPFound(location=next_path)
        else:
            req.session.flash(_('site.application.update.failure'),
                              queue='failure', allow_duplicate=False)

    return dict(form=form, project=project, site=site,
                application=site.application)


@view_config(route_name='console.site.application.view.result',
             renderer=tpl('view_result.mako', type_='application'))
@login_required
def application_site_view_result(req):
    """Renders a site result by id."""
    if 'type' not in req.params or req.params['type'] != 'application':
        raise HTTPNotFound

    project_id = req.matchdict.get('project_id')
    site_id = req.matchdict.get('id')

    project = fetch_project(project_id, req.user.id)
    try:
        site = Site.by_type(req.params['type']).where(
            Site.id == site_id,
            Site.project_id == project_id).get()  # pylint: disable=no-member
    except site.DoesNotExist:
        raise HTTPFound

    return dict(project=project, site=site,
                application=site.application)


@view_config(route_name='console.site.application.view.script',
             renderer=tpl('view_script.mako', type_='application'))
@login_required
def application_site_view_script(req):
    """Renders a site script by id."""
    if 'type' not in req.params or req.params['type'] != 'application':
        raise HTTPNotFound

    project_id = req.matchdict.get('project_id')
    site_id = req.matchdict.get('id')

    project = fetch_project(project_id, req.user.id)
    site = Site.by_type(req.params['type']).where(
        Site.id == site_id,
        Site.project_id == project_id).get()  # pylint: disable=no-member

    replicator = req.find_service(iface=IReplicator, name='site')
    replicator.assign(obj=site)

    return dict(project=project, site=site,
                application=site.application,
                replication_state=replicator.validate())


@view_config(route_name='console.site.application.view.badge',
             renderer=tpl('view_badge.mako', type_='application'))
@login_required
def application_site_view_badge(req):
    """Renders badge view for this site."""
    if 'type' not in req.params or req.params['type'] != 'application':
        raise HTTPNotFound

    project_id = req.matchdict.get('project_id')
    site_id = req.matchdict.get('id')

    project = fetch_project(project_id, req.user.id)
    try:
        site = Site.by_type(req.params['type']).where(
            Site.id == site_id,
            Site.project_id == project_id).get()  # pylint: disable=no-member
    except Site.DoesNotExist:  # pylint: disable=no-member
        raise HTTPNotFound

    return dict(project=project, site=site,
                application=site.application)
