from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from aarau.views.filter import login_required
from aarau.models import (
    Publication,
    Site,
)
from aarau.services.interface import IReplicator

from aarau.views.console.site import (
    get_project,
    get_site,
    tpl,
)
from aarau.views.console.site.form import (
    build_new_publication_site_form,
    build_edit_publication_site_form,
)


@view_config(route_name='console.site.publication.new',
             renderer=tpl('new.mako', type_='publication'))
@login_required
def publication_site_new(req):
    project_id = req.matchdict.get('project_id')
    project = get_project(project_id, user_id=req.user.id)
    site = Site(
        project=project,
        hosting_type='Publication',
        calculation_state='off',
    )
    form = build_new_publication_site_form(req)
    if 'submit' in req.POST:
        _ = req.translate
        if form.validate():
            with req.db.cardinal.atomic():
                pub_f = form.publication.form
                publication = Publication(
                    classification=pub_f.classification.data,
                    name=pub_f.name.data,
                    license=pub_f.license.data,
                    copyright=pub_f.copyright.data,
                    description=pub_f.description.data)
                publication.save()

                site.hosting_id = publication.id
                site.slug = form.slug.data
                site.read_key = Site.grab_unique_key('read_key')
                site.write_key = Site.grab_unique_key('write_key')
                site.save()

            replicator = req.find_service(iface=IReplicator, name='site')
            replicator.assign(obj=site)
            replicator.replicate()

            req.session.flash(_('site.publication.creation.success'),
                              queue='success', allow_duplicate=False)
            next_path = req.route_path('console.project.view', id=project.id)
            return HTTPFound(location=next_path)
        else:
            req.session.flash(_('site.publication.creation.failure'),
                              queue='failure', allow_duplicate=False)

    return dict(form=form, project=project, site=site)


@view_config(route_name='console.site.publication.edit',
             renderer=tpl('edit.mako', type_='publication'))
@login_required
def publication_site_edit(req):
    project_id = req.matchdict.get('project_id')
    site_id = req.matchdict.get('id')

    project = get_project(project_id, user_id=req.user.id)
    site = get_site(site_id, project_id=project.id, type_='publication')

    form = build_edit_publication_site_form(req, site)
    if 'submit' in req.POST:
        _ = req.translate
        if form.validate():
            with req.db.cardinal.atomic():
                pub_f = form.publication.form
                site.publication.classification = pub_f.classification.data
                site.publication.name = pub_f.name.data
                site.publication.license = pub_f.license.data
                site.publication.copyright = pub_f.copyright.data
                site.publication.description = pub_f.description.data
                site.publication.save()

                site.slug = form.slug.data
                site.save()

            replicator = req.find_service(iface=IReplicator, name='site')
            replicator.assign(obj=site)
            replicator.replicate()

            req.session.flash(_('site.publication.update.success'),
                              queue='success', allow_duplicate=False)
            next_path = req.route_path('console.project.view', id=project.id)
            return HTTPFound(location=next_path)
        else:
            req.session.flash(_('site.publication.update.failure'),
                              queue='failure', allow_duplicate=False)

    return dict(form=form, project=project, site=site,
                publication=site.publication)


@view_config(route_name='console.site.publication.view',
             renderer=tpl('view.mako', type_='publication'))
@login_required
def publication_site_view(req):
    project_id = req.matchdict.get('project_id')
    site_id = req.matchdict.get('id')

    project = get_project(project_id, user_id=req.user.id)
    site = get_site(site_id, project_id=project.id, type_='publication')

    return dict(project=project, site=site,
                publication=site.publication)
