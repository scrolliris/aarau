from pyramid.httpexceptions import HTTPNotFound

from aarau.models import (
    Project,
    Membership,
    User,
)


def fetch_project(project_id, user_id):
    project = Project.select().join(Membership).join(User).where(
        User.id == user_id,
        Project.id == project_id
    ).first()
    if not project:
        raise HTTPNotFound
    return project


def tpl(path, type_=''):
    return 'aarau:templates/console/site/{0:s}/{1:s}'.format(type_, path)


def includeme(config):
    config.include('.application')
