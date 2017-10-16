import pytest
from webob.multidict import MultiDict


@pytest.fixture(autouse=True)
def setup(request, config, mailer_outbox):
    def clean_outbox():
        del mailer_outbox[:]
    clean_outbox()

    # eager task (emulation)
    from aarau.tasks import worker
    worker.conf.update(task_always_eager=True)

    def teardown():
        worker.conf.update(task_always_eager=False, task_eager_propagates=True)
        clean_outbox()

    request.addfinalizer(teardown)


def test_signup_with_logged_in_user(users, dummy_request):
    from aarau.views.signup.action import signup

    dummy_request.user = users['oswald']
    res = signup(dummy_request)

    assert '302 Found' == res.status
    assert '/' == res.location
    assert not dummy_request.session.pop_flash('failure')
    assert 'Set-Cookie' not in res.headers


def test_signup_with_none_submitted_request(dummy_request):
    from aarau.views.signup.action import signup
    from aarau.views.signup.form import SignupForm

    dummy_request.user = None
    dummy_request.params = dummy_request.POST = MultiDict()
    res = signup(dummy_request)

    assert isinstance(res['form'], SignupForm)
    assert not dummy_request.session.pop_flash('failure')


def test_signup_with_validation_error(users, dummy_request):
    from aarau.views.signup.action import signup
    from aarau.views.signup.form import SignupForm

    user = {
        'name': 'Hennnry the Penguin',
        'username': 'hennnry',
        'email': 'henry@example.org',  # alredy exists!
        'password': 'SloooowAndSteady5',
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

    assert isinstance(res['form'], SignupForm)
    assert dummy_request.session.pop_flash('failure')


def test_signup_with_valid_credentials(users, dummy_request):
    from aarau.views.signup.action import signup

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

    assert '302 Found' == res.status
    assert '/signup' == res.location
    assert not dummy_request.session.pop_flash('failure')
    assert 'Set-Cookie' not in res.headers
