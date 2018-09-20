from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound, HTTPNotFound

from aarau.views.filter import login_required
from aarau.models import Site
from aarau.services.interface import IManager

from aarau.views import get_site_type

from aarau.models import Classification
from aarau.queries.project import get_project
from aarau.queries.site import get_site
from aarau.views.console.site import tpl
from aarau.views.console.site.form import build_site_form


def build_instance_of(site, form):
    instance = site.instance

    if instance is None:
        instance = site.instantiate()

    instance.name = form.name.data
    instance.description = form.description.data

    if site.type == 'publication':
        c = Classification.find_by_notation(form.classification.data)
        instance.classification = c.id
        instance.license = form.license.data
        instance.copyright = form.copyright.data

    return instance


@view_config(route_name='console.site.new', renderer='.mako')
@login_required
def site_new(req):
    site_type = get_site_type(req.params)
    namespace = req.matchdict.get('namespace')

    project = get_project(namespace, user=req.user)
    site = Site(
        project=project,
        instance_type=site_type.capitalize(),
        calculation_state='off',
    )

    # create
    form = build_site_form(req, site)
    if 'submit' in req.POST:
        _ = req.translate
        if form.validate():
            with req.db.cardinal.atomic():
                instance = build_instance_of(site, form.instance.form)
                instance.save()

                site.slug = form.slug.data
                site.instance_id = instance.id
                site.read_key = Site.grab_unique_key('read_key')
                site.write_key = Site.grab_unique_key('write_key')

                if site.type == 'application':
                    site.domain = form.domain.data

                site.save()

            manager = req.find_service(iface=IManager, name='credentials')
            manager.assign(obj=site)
            manager.sync()

            req.session.flash(
                _('site.{:s}.creation.success'.format(site.type)),
                queue='success', allow_duplicate=False)
            next_path = req.route_path(
                'console.project.overview', namespace=project.namespace)
            return HTTPFound(location=next_path)

        req.session.flash(
            _('site.{:s}.creation.failure'.format(site.type)),
            queue='failure', allow_duplicate=False)

    req.override_renderer = tpl('new.mako', type_=site.type)
    return dict(form=form, project=project, site=site)


@view_config(route_name='console.site.overview', renderer='.mako')
@login_required
def site_overview(req):
    namespace = req.matchdict.get('namespace')
    slug = req.matchdict.get('slug')

    project = get_project(namespace, user=req.user)
    site = get_site(slug, project=project)

    req.override_renderer = tpl('overview.mako', type_=site.type)
    return dict(project=project, site=site, instance=site.instance)


@view_config(route_name='console.site.insights',
             renderer=tpl('insights.mako', type_='application'))
@login_required
def site_insights(req):
    namespace = req.matchdict.get('namespace')
    slug = req.matchdict.get('slug')

    project = get_project(namespace, user=req.user)
    site = get_site(slug, project=project)

    component_type = 'metrics'
    if 'tab' in req.params and req.params['tab'] == 'logs':
        component_type = 'logs'

    # only application
    return dict(project=project, site=site, instance=site.instance,
                component_type=component_type)


@view_config(route_name='console.site.settings',
             request_method=('GET', 'POST'), renderer=tpl('.mako'))
@login_required
def site_settings(req):
    namespace = req.matchdict.get('namespace')
    slug = req.matchdict.get('slug')

    project = get_project(namespace, user=req.user)
    site = get_site(slug, project=project)

    # update
    form = build_site_form(req, site)
    if 'submit' in req.POST:
        _ = req.translate
        if form.validate():
            update_slug = False

            with req.db.cardinal.atomic():
                instance = build_instance_of(site, form.instance.form)
                instance.save()

                if site.slug != form.slug.data:
                    update_slug = True
                    site.slug = form.slug.data

                if site.type == 'application':
                    site.domain = form.domain.data

                site.save()

            manager = req.find_service(iface=IManager, name='credentials')
            manager.assign(obj=site)
            manager.sync()

            req.session.flash(_('site.{:s}.update.success'.format(site.type)),
                              queue='success', allow_duplicate=False)
            if update_slug:
                next_path = req.route_path(
                    'console.site.settings', namespace=project.namespace,
                    slug=site.slug)
                return HTTPFound(location=next_path)
        else:
            req.session.flash(_('site.{:s}.update.failure'.format(site.type)),
                              queue='failure', allow_duplicate=False)

    req.override_renderer = tpl('settings.mako', type_=site.type)
    return dict(project=project, site=site, form=form, instance=site.instance)


@view_config(route_name='console.site.settings.scripts',
             renderer=tpl('settings_scripts.mako', type_='application'))
@login_required
def site_settings_scripts(req):
    namespace = req.matchdict.get('namespace')
    slug = req.matchdict.get('slug')

    project = get_project(namespace, user=req.user)
    site = get_site(slug, project=project)

    if site.type != 'application':
        raise HTTPNotFound

    manager = req.find_service(iface=IManager, name='credentials')
    manager.assign(obj=site)

    # only application
    return dict(project=project, site=site, instance=site.instance,
                credentials_state=manager.validate('write'))


@view_config(route_name='console.site.settings.widgets',
             renderer=tpl('settings_widgets.mako', type_='application'))
@login_required
def site_settings_widgets(req):
    namespace = req.matchdict.get('namespace')
    slug = req.matchdict.get('slug')

    project = get_project(namespace, user=req.user)
    site = get_site(slug, project=project)

    if site.type != 'application':
        raise HTTPNotFound

    manager = req.find_service(iface=IManager, name='credentials')
    manager.assign(obj=site)

    # only application
    return dict(project=project, site=site, instance=site.instance,
                credentials_state=manager.validate('read'))


@view_config(route_name='console.site.settings.badges',
             renderer=tpl('settings_badges.mako', type_='application'))
@login_required
def site_settings_badges(req):
    namespace = req.matchdict.get('namespace')
    slug = req.matchdict.get('slug')

    project = get_project(namespace, user=req.user)
    site = get_site(slug, project=project)

    return dict(project=project, site=site, instance=site.instance)
