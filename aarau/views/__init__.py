from pyramid.events import subscriber
from pyramid.events import BeforeRender


@subscriber(BeforeRender)
def add_article_renderer_globals(evt) -> None:
    """Adds global variables for article (public reader) renderer."""
    req = evt['request']

    if req and not req.subdomain:
        evt['cookie'] = {'article.sidebar': ''}
        key = 'article.sidebar'
        if key in req.cookies:
            evt['cookie'][key] = str(req.cookies[key])


def tpl(path, resource=None):
    """Returns template path from package root."""
    if resource:
        return 'aarau:templates/{0:s}/{1:s}'.format(resource, path)

    return 'aarau:templates/{0:s}'.format(path)


def subdomain(request):
    """Returns subdomain from `request.domain`."""
    if request.domain == request.settings.get('domain.application', None):
        return None

    parts = request.domain.split('.', 2)
    if not len(parts) >= 3:
        return None
    return parts[0]


def get_site_type(params):
    # fmt: off
    site_type = 'publication' if (
        'type' not in params or params['type'] == 'publication'
    ) else 'application'
    # fmt: on
    return site_type


def includeme(config):
    """Initializes views for aarau app.

    Activate this setup using ``config.include('aarau.views')``.
    """
    config.include('.signup')

    config.include('.project')

    config.include('.site')
    config.include('.article')

    # subdomains
    config.include('.console')
    config.include('.carrell')
    config.include('.registry')

    # make request.subdomain available for use in app
    config.add_request_method(subdomain, 'subdomain', reify=True)
