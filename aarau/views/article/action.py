from pyramid.view import view_config
from pyramid.httpexceptions import (
    HTTPFound,
    HTTPNotFound
)

from aarau.models import (
    Article,
    Site,
)
from aarau.views import tpl
from aarau.queries.site import get_sites


@view_config(route_name='article', renderer=tpl('article/view.mako'))
def article_view(req):
    slug = req.matchdict.get('slug')
    path = req.matchdict.get('path')

    if req.user:
        next_path = req.route_url('carrell.top')
        raise HTTPFound(location=next_path)

    try:
        site = get_sites('publication', limit=1).where(
            Site.slug == slug
        ).get()
        publication = site.instance
        article = publication.articles.where(
            Article.path == path,
            Article.scope == 'public',
            Article.progress_state == 'published',
        ).get()
    except Article.DoesNotExist:
        raise HTTPNotFound

    return dict(site=site, publication=publication, article=article)
