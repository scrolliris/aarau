# pylint: disable=invalid-name
"""Route Tests.
"""
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


def test_routing_to_favicon_ico(dummy_app):
    """Test Routing /favicon.ico.
    """
    res = dummy_app.get('/favicon.ico', status=200)
    assert 200 == res.status_code


@pytest.mark.usefixtures('login')
def test_routing_to_favicon_ico_as_logged_in_user(dummy_app):
    """Test Routing /favicon.ico as logged in user.
    """
    res = dummy_app.get('/favicon.ico', status=200)
    assert 200 == res.status_code


def test_routing_to_humans_txt(dummy_app):
    """Test Routing /humans.txt.
    """
    res = dummy_app.get('/humans.txt', status=200)
    assert 200 == res.status_code


@pytest.mark.usefixtures('login')
def test_routing_to_humans_txt_as_logged_in_user(dummy_app):
    """Test Routing /humans.txt as logged in user.
    """
    res = dummy_app.get('/humans.txt', status=200)
    assert 200 == res.status_code


def test_routing_to_robots_txt(dummy_app):
    """Test Routing /robots.txt.
    """
    res = dummy_app.get('/robots.txt', status=200)
    assert 200 == res.status_code


@pytest.mark.usefixtures('login')
def test_routing_to_robots_txt_as_logged_in_user(dummy_app):
    """Test Routing /robots.txt as logged in user.
    """
    res = dummy_app.get('/robots.txt', status=200)
    assert 200 == res.status_code
