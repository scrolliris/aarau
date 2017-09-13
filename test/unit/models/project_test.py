# pylint: disable=unused-argument,invalid-name
"""Unit test for project model.
"""
import pytest

from aarau.models import Project


@pytest.fixture(autouse=True)
def setup(config):
    """Setup.
    """
    pass


def test_primary_owner(projects, plans, users):
    """Test primary ownership after creation.
    """
    from aarau.models import Membership

    project = projects['piano-music-club']
    assert users['oswald'] == project.primary_owner

    # new
    user = users['weenie']
    plan = plans['plan.academic.name']
    project = Project(
        plan=plan, name='Bow!', namespace='bowow', copyright='2017 Weenie')
    project.access_key_id = Project.grab_unique_key('access_key_id')
    project.save()

    # create membership
    project.users.add(user)
    assert project == user.projects.where(Project.namespace == 'bowow').get()

    membership = user.memberships.where(
        Membership.project_id == project.id  # pylint: disable=no-member
    ).first()

    # default role
    assert 'member' == membership.role

    with pytest.raises(user.__class__.DoesNotExist):
        project.primary_owner

    membership.role = 'primary_owner'
    membership.save()

    assert user == project.primary_owner
