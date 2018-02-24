from pyramid.httpexceptions import HTTPNotFound

from aarau.models import (
    Project,
    Membership,
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
