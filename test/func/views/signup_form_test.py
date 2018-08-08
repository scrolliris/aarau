import pytest

from webob.multidict import MultiDict

from aarau.views.signup.form import build_signup_form


@pytest.fixture(autouse=True)
def setup(request, config):  # pylint: disable=unused-argument
    pass

# username


@pytest.mark.parametrize('username', [
    'ai',
    'k_',
    'bob',
    'b00',
])
def test_username_min_length_errors(username, dummy_request):
    dummy_request.params = dummy_request.POST = MultiDict({
        'csrf_token': dummy_request.session.get_csrf_token(),
        'username': username,
    })
    form = build_signup_form(dummy_request)

    assert not form.validate()
    assert ['Field must be between 4 and 16 characters long.'] == \
        form.username.errors


@pytest.mark.parametrize('username', [
    'loooooooooooooong',
    'l_______________g',
    'loooooooooooooog_',
])
def test_username_max_length_errors(username, dummy_request):
    dummy_request.params = dummy_request.POST = MultiDict({
        'csrf_token': dummy_request.session.get_csrf_token(),
        'username': username,
    })
    form = build_signup_form(dummy_request)

    assert not form.validate()
    assert ['Field must be between 4 and 16 characters long.'] == \
        form.username.errors


@pytest.mark.parametrize('username', [
    '0abc',
    'Abcd',
    '_bcd',
    'abCd',
    'abc*',
])
def test_username_invalid_pattern_errors(username, dummy_request):
    dummy_request.params = dummy_request.POST = MultiDict({
        'csrf_token': dummy_request.session.get_csrf_token(),
        'username': username,
    })
    form = build_signup_form(dummy_request)

    assert not form.validate()
    assert [('You must use only lowercase alphanumeric characters, and '
             'start with a-z')] == form.username.errors


@pytest.mark.parametrize('username', [
    'i',
    '00',
    'Abc',
    '_bc',
    'abC',
])
def test_username_invalid_pattern_and_min_length_errors(
        username, dummy_request):
    dummy_request.params = dummy_request.POST = MultiDict({
        'csrf_token': dummy_request.session.get_csrf_token(),
        'username': username,
    })
    form = build_signup_form(dummy_request)

    assert not form.validate()
    assert [('You must use only lowercase alphanumeric characters, and '
             'start with a-z'),
            'Field must be between 4 and 16 characters long.'] == \
        form.username.errors


@pytest.mark.parametrize('username', [
    'oswald',
    'weenie',
    'henry',
    'daisy',
    'johnny',
])
def test_username_unique_check_errors(username, dummy_request):
    dummy_request.params = dummy_request.POST = MultiDict({
        'csrf_token': dummy_request.session.get_csrf_token(),
        'username': username,
    })
    form = build_signup_form(dummy_request)

    assert not form.validate()
    assert ['This username is already taken'] == form.username.errors


def test_username_reserved_word_errors():
    # TODO
    pass


def test_username_optionality(dummy_request):
    dummy_request.params = dummy_request.POST = MultiDict({
        'csrf_token': dummy_request.session.get_csrf_token(),
        # 'username': '',
    })
    form = build_signup_form(dummy_request)

    assert not form.validate()
    assert not form.username.errors
