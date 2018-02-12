from pyramid.view import view_config
from pyramid.httpexceptions import (
    HTTPFound,
    HTTPNotFound
)

from aarau.models import (
    Article,
    Site,
    Project,
)
from aarau.queries.site import get_sites
from aarau.views import tpl


@view_config(route_name='carrell.read',
             renderer=tpl('read.mako', resource='carrell'))
# @login_required # check in the action
def read(req):
    namespace = req.params.get('namespace')
    slug = req.params.get('slug')
    path = req.params.get('path')
    if not req.user:
        next_path = req.route_url(
            'article', namespace=namespace, slug=slug, path=path)
        raise HTTPFound(location=next_path)

    try:
        # TODO: refactor
        project = Project.select().where(
            Project.namespace == namespace).get()
        site = get_sites('publication', limit=1).where(
            Site.slug == slug,
            Site.project_id == project.id,
        ).get()
        publication = site.instance
        article = publication.articles.where(
            Article.publication_id == publication.id,
            Article.path == path,
            Article.scope == 'public',
            Article.progress_state == 'published',
        ).get()
    except Article.DoesNotExist:
        raise HTTPNotFound

    return dict(site=site, publication=publication, article=article)
