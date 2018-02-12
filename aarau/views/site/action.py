from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound

from aarau.models import (
    Site,
)
from aarau.views import tpl
from aarau.queries.site import get_sites


@view_config(route_name='publication', renderer=tpl('site/view.mako'))
def publication_view(req):
    slug = req.matchdict.get('slug')

    try:
        site = get_sites('publication', limit=1).where(
            Site.slug == slug
        ).get()
    except Site.DoesNotExist:
        raise HTTPNotFound

    publication = site.instance
    articles = [a for a in publication.articles
                if a.scope == 'public' and a.progress_state == 'published']
    return dict(site=site, publication=publication, articles=articles)
