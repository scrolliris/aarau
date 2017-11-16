from pyramid.httpexceptions import HTTPNotFound

from aarau.models import (
    Project,
    Membership,
    Site,
    User,
)


def get_project(project_id, user_id=None):
    """Gets a project belongs to user.

    If it does not exist, raises HTTPNotFound error.
    """
    project = Project.select().join(Membership).join(User).where(
        User.id == user_id,
        Project.id == project_id
    ).first()
    if not project:
        raise HTTPNotFound
    return project


def get_site(site_id, project_id=None, type_=''):
    """Gets a site by type belongs to porject.

    If it does not exist, raises HTTPNotFound error.
    """
    try:
        site = Site.by_type(type_).where(
            Site.id == site_id,
            Site.project_id == project_id).get()  # pylint: disable=no-member
    except Site.DoesNotExist:  # pylint: disable=no-member
        raise HTTPNotFound
    return site


def tpl(path, type_=''):
    return 'aarau:templates/console/site/{0:s}/{1:s}'.format(type_, path)


def includeme(config):
    config.include('.application')
    config.include('.publication')
