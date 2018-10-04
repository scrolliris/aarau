from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound

from peewee import fn, JOIN

from aarau.models.chapter import Chapter
from aarau.models.article import Article
from aarau.models.publication import Publication
from aarau.queries.project import get_project
from aarau.queries.site import get_site
from aarau.views.filter import login_required
from aarau.views.console.chapter import tpl


@view_config(route_name='console.chapter.tree',
             renderer=tpl('tree.mako'))
@login_required
def chapter_tree(req):
    namespace = req.matchdict.get('namespace')
    slug = req.matchdict.get('slug')

    project = get_project(namespace, user=req.user)
    site = get_site(slug, project=project)

    if site.type != 'publication':
        raise HTTPNotFound

    publication = site.instance
    chapters = Chapter.select(
        Chapter,
        fn.COUNT(Article.id).alias('articles_count')
    ).join(Article, JOIN.LEFT_OUTER).join(
        Publication, on=(Chapter.publication_id == publication.id)
    ).group_by(
        Chapter.id
    ).order_by(
        Chapter.name.asc(),
    )

    return dict(
        project=project,
        site=site,
        publication=publication,
        chapters=chapters)


@view_config(route_name='console.chapter.edit',
             renderer=tpl('edit.mako'))
@login_required
def chapter_edit(req):
    namespace = req.matchdict.get('namespace')
    slug = req.matchdict.get('slug')
    chapter_slug = req.matchdict.get('chapter_slug')

    project = get_project(namespace, user=req.user)
    site = get_site(slug, project=project)

    if site.type != 'publication':
        raise HTTPNotFound

    publication = site.instance
    try:
        chapter = Chapter.select(
            Chapter,
            fn.COUNT(Article.id).alias('articles_count')
        ).join(Article, JOIN.LEFT_OUTER).join(
            Publication, on=(Chapter.publication_id == publication.id)
        ).where(
            Chapter.slug == chapter_slug
        ).group_by(
            Chapter.id
        ).order_by(
            Chapter.name.asc(),
        ).get()
    except Chapter.DoesNotExist:
        raise HTTPNotFound

    return dict(
        project=project,
        site=site,
        publication=publication,
        chapter=chapter)
