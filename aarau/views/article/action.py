from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound

from aarau.models import Article, Project, Site
from aarau.views import tpl
from aarau.queries.site import get_sites


@view_config(route_name='article', renderer=tpl('article/view.mako'))
def article_view(req):
    namespace = req.matchdict.get('namespace')
    slug = req.matchdict.get('slug')
    path = req.matchdict.get('path')

    try:
        project = Project.select().where(Project.namespace == namespace).get()

        # fmt: off
        site = get_sites('publication', limit=1).where(
            Site.slug == slug,
            Site.project_id == project.id,
        ).get()
        # fmt: on

        publication = site.instance
        article = publication.articles.where(
            Article.path == path,
            Article.scope == 'public',
            Article.progress_state == 'published',
        ).get()
    except Article.DoesNotExist:
        raise HTTPNotFound

    return dict(site=site, publication=publication, article=article)
