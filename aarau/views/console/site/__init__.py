from pyramid.httpexceptions import HTTPNotFound

from aarau.models import (
    Project,
    Membership,
    Site,
    User,
)


def get_project(namespace, user=None):
    """Gets a project belongs to the user.

    If it does not exist, raises HTTPNotFound error.
    """
    if not user:
        return None
    project = Project.select().join(Membership).join(User).where(
        User.id == user.id,
        Project.namespace == namespace
    ).first()
    if not project:
        raise HTTPNotFound
    return project


def get_site(slug, project=None):
    """Gets a site by type belongs to the porject.

    If it does not exist, raises HTTPNotFound error.
    """
    if not project:
        return None
    try:
        site = Site.select().where(
            Site.slug == slug,
            Site.project_id == project.id).get()  # pylint: disable=no-member
    except Site.DoesNotExist:  # pylint: disable=no-member
        raise HTTPNotFound
    return site


def tpl(path, type_=''):
    """Genarets template path by instance type."""
    return 'aarau:templates/console/site/{0:s}/{1:s}'.format(type_, path)


def includeme(_config):
    pass
