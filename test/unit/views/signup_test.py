import pytest


@pytest.fixture(autouse=True)
def setup(request, config, mailer_outbox):
    def clean_outbox():
        del mailer_outbox[:]
    clean_outbox()

    # eager task (emulation)
    from aarau.tasks import worker
    worker.conf.update(task_always_eager=True)

    def teardown():
        worker.conf.update(task_always_eager=False)
        clean_outbox()

    request.addfinalizer(teardown)


def test_signup_with_valid_credentials(users, dummy_request):
    from webob.multidict import MultiDict
    from aarau.views.signup.actions import signup

    user = {  # The Egg Twins
        'name': 'Leo The Egg Twins',
        'username': 'leotheegg',
        'email': 'leo@example.org',
        'password': 'Yes*2!',
    }

    dummy_request.user = None
    dummy_request.params = dummy_request.POST = MultiDict({
        'submit': '1',
        'csrf_token': dummy_request.session.get_csrf_token(),
        'name': user['name'],
        'username': user['username'],
        'email': user['email'],
        'password': user['password'],
    })
    res = signup(dummy_request)

    assert not dummy_request.session.pop_flash('error')
    assert '302 Found' == res.status
    assert '/login' == res.location

    # doesn't login yet
    assert 'Set-Cookie' not in res.headers
