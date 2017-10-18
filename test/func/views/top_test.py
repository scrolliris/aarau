import pytest


@pytest.fixture(autouse=True)
def setup(request, config):  # pylint: disable=unused-argument
    # eager task (emulation)
    from aarau.tasks import worker
    worker.conf.update(task_always_eager=True)

    def teardown():
        worker.conf.update(task_always_eager=False)

    request.addfinalizer(teardown)


def test_top(dummy_app):
    res = dummy_app.get('/', status=200)
    assert b'Scrolliris' in res.body


@pytest.mark.usefixtures('login')
def test_top_as_logged_in_user(dummy_app):
    res = dummy_app.get('/', status=200)
    assert b'Scrolliris' in res.body
