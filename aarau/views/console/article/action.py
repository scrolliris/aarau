from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound

from aarau.models.article import Article
from aarau.queries.project import get_project
from aarau.queries.site import get_site
from aarau.views.filter import login_required
from aarau.views.console.article import tpl
from aarau.views.console.article.form import (
    build_article_editor_form,
    build_article_settings_form,
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


@view_config(route_name='console.article.editor.new',
             request_method='GET', renderer=tpl('editor.mako'))
@view_config(route_name='console.article.editor.edit',
             request_method='GET', renderer=tpl('editor.mako'))
@login_required
def article_editor(req):
    namespace = req.matchdict.get('namespace')
    slug = req.matchdict.get('slug')

    code = req.params.get('code', None)  # update

    project = get_project(namespace, user=req.user)
    site = get_site(slug, project=project)

    if site.type != 'publication':
        raise HTTPNotFound

    publication = site.instance
    if code:
        article = publication.articles.where(Article.code == code).get()
    else:
        code = Article.grab_unique_code()  # as path
        article = Article(path=code, code=code)

    editor_form = build_article_editor_form(req, article)
    settings_form = build_article_settings_form(req, article)

    return dict(
        editor_form=editor_form,
        settings_form=settings_form,
        project=project,
        site=site,
        publication=publication,
        article=article,
    )
