""" View action package
"""


def tpl(path, namespace=None):
    """ Returns template path from package root
    """
    if namespace:
        return 'aarau:templates/{0:s}/{1:s}'.format(namespace, path)
    else:
        return 'aarau:templates/{0:s}'.format(path)


def subdomain(request):
    """ Returns subdomain from `request.domain`
    """
    if request.domain == request.settings.get('domain.application', None):
        return None

    parts = request.domain.split('.', 2)
    if not len(parts) >= 3:
        return None
    return parts[0]


def includeme(config):
    """ Initializes the view for a aarau app

    Activate this setup using ``config.include('aarau.views')``.
    """
    config.include('.signup')
    config.include('.settings')
    config.include('.console')

    # make request.subdomain available for use in app
    config.add_request_method(subdomain, 'subdomain', reify=True)
