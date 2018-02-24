def tpl(path, type_=''):
    """Genarets template path by instance type."""
    if type_ != '':
        type_ += '/'
    return 'aarau:templates/console/article/{0:s}{1:s}'.format(type_, path)


def includeme(_config):
    pass
