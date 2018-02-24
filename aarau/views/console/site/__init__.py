def tpl(path, type_=''):
    """Genarets template path by instance type."""
    return 'aarau:templates/console/site/{0:s}/{1:s}'.format(type_, path)


def includeme(_config):
    pass
