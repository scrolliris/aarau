def tpl(path, resource='settings'):
    return 'aarau:templates/carrell/{0:s}/{1:s}'.format(resource, path)


def includeme(config):  # pylint: disable=unused-argument
    pass
