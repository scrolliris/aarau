def tpl(path, resource='project'):
    return 'aarau:templates/console/{0:s}/{1:s}'.format(resource, path)


def includeme(config):  # pylint: disable=unused-argument
    pass
