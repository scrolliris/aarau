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
    site_type = 'publication' if (
        'type' not in params or params['type'] == 'publication'
    ) else 'application'
    return site_type


def includeme(config):
    """Initializes views for aarau app.

    Activate this setup using ``config.include('aarau.views')``.
    """
    config.include('.signup')
    config.include('.settings')

    config.include('.project')
    config.include('.site')

    config.include('.console')

    # make request.subdomain available for use in app
    config.add_request_method(subdomain, 'subdomain', reify=True)
