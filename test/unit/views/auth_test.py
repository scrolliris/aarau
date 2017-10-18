import re

import pytest

TKT = re.compile(r'auth_tkt=[A-z0-9_\!\:]+;')


@pytest.fixture(autouse=True)
def setup(config):  # pylint: disable=unused-argument
    pass


def test_login(dummy_request):
    from aarau.views.auth import login

    referrer = 'http://example.org/'
    dummy_request.user = None
    dummy_request.referrer = referrer
    res = login(dummy_request)

    assert {'email': '', 'next_path': referrer} == res


def test_login_as_logged_in_user_with_referrer(
        users, dummy_request):
    from aarau.views.auth import login

    referrer = 'http://example.org/settings'
    dummy_request.user = users['oswald']
    dummy_request.referrer = referrer
    res = login(dummy_request)

    assert '302 Found' == res.status
    assert referrer == res.location

    assert TKT.match(res.headers['Set-Cookie'])


def test_login_as_logged_in_user_without_referrer(
        users, dummy_request):
    from aarau.views.auth import login

    dummy_request.user = users['oswald']
    dummy_request.referrer = None
    res = login(dummy_request)

    assert '302 Found' == res.status
    assert '/' == res.location

    assert TKT.match(res.headers['Set-Cookie'])


def test_login_with_wrong_email(dummy_request):
    from aarau.views.auth import login

    dummy_request.user = None
    dummy_request.referrer = None
    dummy_request.params = dummy_request.POST = {
        'submit': '1',
        'email': 'unknown',
        'password': '0PlayingPiano'
    }
    res = login(dummy_request)

    assert 'The credential you\'ve entered is incorrect' == \
           dummy_request.session.pop_flash('failure')[0]
    assert 'unknown' == res['email']


def test_login_with_wrong_password(users, dummy_request):
    from aarau.views.auth import login

    user = users['oswald']
    dummy_request.user = None
    dummy_request.referrer = None
    dummy_request.params = dummy_request.POST = {
        'submit': '1',
        'email': user.email,
        'password': 'invalid',
    }
    res = login(dummy_request)

    assert 'The credential you\'ve entered is incorrect' == \
           dummy_request.session.pop_flash('failure')[0]
    assert user.email == res['email']


def test_login_as_pending_user(users, dummy_request):
    from aarau.views.auth import login

    user = users['johnny']
    dummy_request.user = None
    dummy_request.referrer = None
    dummy_request.params = dummy_request.POST = {
        'submit': '1',
        'email': user.email,
        'password': '1ceCreame',
    }
    res = login(dummy_request)

    assert 'The credential you\'ve entered is incorrect' == \
           dummy_request.session.pop_flash('failure')[0]
    assert user.email == res['email']


def test_login_with_valid_credentials(users, dummy_request):
    from aarau.views.auth import login

    user = users['oswald']
    dummy_request.user = None
    dummy_request.referrer = None
    dummy_request.params = dummy_request.POST = {
        'submit': '1',
        'email': user.email,
        'password': '0PlayingPiano'
    }
    res = login(dummy_request)

    assert not dummy_request.session.pop_flash('failure')
    assert '302 Found' == res.status
    assert '/' == res.location

    assert TKT.match(res.headers['Set-Cookie'])


def test_logout_as_logged_in_user(users, dummy_request):
    from aarau.views.auth import login, logout

    dummy_request.user = users['oswald']
    dummy_request.referrer = None
    res = login(dummy_request)

    assert '302 Found' == res.status
    assert '/' == res.location
    assert TKT.match(res.headers['Set-Cookie'])

    res = logout(dummy_request)

    assert '302 Found' == res.status
    assert 'http://example.org/' == res.location
    # it should be empty
    assert 'auth_tkt=;' in res.headers['Set-Cookie']
