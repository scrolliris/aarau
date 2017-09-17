# pylint: disable=invalid-name
"""Route Tests.
"""
import os
import pytest


@pytest.fixture(autouse=True)
def setup(request, config):  # pylint: disable=unused-argument
    """The setup.
    """
    # eager task (emulation)
    from aarau.tasks import worker
    worker.conf.update(task_always_eager=True)

    def teardown():
        """The teardown.
        """
        worker.conf.update(task_always_eager=False)

    request.addfinalizer(teardown)


def test_routing_to_favicon(dummy_app):
    """Test Routing /favicon.ico.
    """
    res = dummy_app.get('/favicon.ico', status=200)
    assert 200 == res.status_code


@pytest.mark.usefixtures('login')
def test_routing_to_favicon_as_logged_in_user(dummy_app, login_as, users):
    """Test Routing /favicon.ico as logged in user.
    """
    user = users['oswald']
    with login_as(user):
        app = dummy_app.switch_target('console')
        res = app.get('/favicon.ico', status=200)
        assert 200 == res.status_code


def test_routing_to_humans(dummy_app):
    """Test Routing /humans.txt.
    """
    res = dummy_app.get('/humans.txt', status=200)
    assert 200 == res.status_code


def test_routing_to_humans_as_logged_in_user(dummy_app, login_as, users):
    """Test Routing /humans.txt as logged in user.
    """
    user = users['oswald']
    with login_as(user):
        app = dummy_app.switch_target('console')
        res = app.get('/humans.txt', status=200)
        assert 200 == res.status_code


def test_routing_to_robots(dummy_app):
    """Test Routing /robots.txt.
    """
    res = dummy_app.get('/robots.txt', status=200)
    assert 200 == res.status_code


def test_routing_to_robots_as_logged_in_user(dummy_app, login_as, users):
    """Test Routing /robots.txt as logged in user.
    """
    user = users['oswald']
    with login_as(user):
        app = dummy_app.switch_target('console')
        res = app.get('/robots.txt', status=200)
        assert 200 == res.status_code

def test_routing_to_console_application_site_badge(dummy_app, login_as, users):
    """Test touting to badge view as logged in user.
    """
    user = users['oswald']
    with login_as(user):
        project = user.projects[0]
        site = project.application_sites[0]
        url = '/project/{}/site/{}/badge?type=application'.format(
            project.id, site.id)
        app = dummy_app.switch_target('console')
        res = app.get(url, status=200)
        assert 200 == res.status_code
