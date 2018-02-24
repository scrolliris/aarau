from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound, HTTPNotFound

from aarau.models.article import Article
from aarau.queries.project import get_project
from aarau.queries.site import get_site
from aarau.views.filter import login_required
from aarau.views.console.article import tpl
from aarau.views.console.article.form import (
    build_new_article_form,
    build_edit_article_form,
)


@view_config(route_name='console.article.list',
             renderer=tpl('list.mako'))
@login_required
def article_list(req):
    namespace = req.matchdict.get('namespace')
    slug = req.matchdict.get('slug')

    project = get_project(namespace, user=req.user)
    site = get_site(slug, project=project)

    if site.type != 'publication':
        raise HTTPNotFound

    publication = site.instance
    articles = publication.articles

    return dict(
        project=project,
        site=site,
        publication=publication,
        articles=articles)


@view_config(route_name='console.article.new',
             renderer=tpl('new.mako'))
@login_required
def article_new(req):
    namespace = req.matchdict.get('namespace')
    slug = req.matchdict.get('slug')

    project = get_project(namespace, user=req.user)
    site = get_site(slug, project=project)

    if site.type != 'publication':
        raise HTTPNotFound

    publication = site.instance

    # create
    form = build_new_article_form(req)
    if 'submit' in req.POST:
        _ = req.translate
        if form.validate():
            with req.db.cardinal.atomic():
                article = Article(
                    publication=publication,
                    title=form.title.data,
                    path=form.path.data,
                    copyright='',
                    progress_state='draft')
                article.code = Article.grab_unique_code()
                article.save()

            req.session.flash(
                _('article.creation.success'),
                queue='success', allow_duplicate=False)
            next_path = req.route_path(
                'console.article.list',
                namespace=project.namespace, slug=site.slug)
            return HTTPFound(location=next_path)
        else:
            req.session.flash(
                _('article.creation.failure'),
                queue='failure', allow_duplicate=False)
    else:
        form.path.data = Article.grab_unique_code()

    return dict(
        form=form,
        project=project,
        site=site,
        publication=publication)


@view_config(route_name='console.article.edit',
             renderer=tpl('edit.mako'))
@login_required
def article_edit(req):
    namespace = req.matchdict.get('namespace')
    slug = req.matchdict.get('slug')
    path = req.matchdict.get('path')

    project = get_project(namespace, user=req.user)
    site = get_site(slug, project=project)

    if site.type != 'publication':
        raise HTTPNotFound

    publication = site.instance
    article = publication.articles.where(Article.path == path).get()

    # create
    form = build_edit_article_form(req, article)
    if 'submit' in req.POST:
        _ = req.translate
        if form.validate():
            with req.db.cardinal.atomic():
                article.title = form.title.data
                article.save()

            req.session.flash(
                _('article.update.success'),
                queue='success', allow_duplicate=False)
            next_path = req.route_path(
                'console.article.list',
                namespace=project.namespace, slug=site.slug)
            return HTTPFound(location=next_path)
        else:
            req.session.flash(
                _('article.update.failure'),
                queue='failure', allow_duplicate=False)

    return dict(
        form=form,
        project=project,
        site=site,
        publication=publication,
        article=article)
