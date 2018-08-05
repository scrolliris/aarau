from datetime import datetime

import pytest
from webob.multidict import MultiDict
from wtforms import ValidationError

from aarau.models import (
    User,
    UserEmail,
)
from aarau.views.signup.form import (
    build_signup_form,
    SignupForm,
    validate_username_uniqueness,
    validate_email_uniqueness,
    username_availability_check,
)


@pytest.fixture(autouse=True)
def setup(request, config, monkeypatch):  # pylint: disable=unused-argument
    from aarau.views import form
    monkeypatch.setattr(form, 'RESERVED_WORDS_FILE',
                        'aarau:../config/reserved_words.sample.yml')

    def teardown():
        monkeypatch.undo()

    request.addfinalizer(teardown)


def test_build_signup_form(dummy_request):
    dummy_request.params = dummy_request.POST = MultiDict()
    form = build_signup_form(dummy_request)
    assert isinstance(form, SignupForm)


def test_validate_username_uniqueness_with_existing_username(
        mocker, users, dummy_request):
    user = users['oswald']

    dummy_request.params = dummy_request.POST = MultiDict()
    form = build_signup_form(dummy_request)

    with pytest.raises(ValidationError):
        field = mocker.Mock('field', data=user.username)
        validate_username_uniqueness(form, field)


def test_validate_username_uniqueness_with_new_username(mocker, dummy_request):
    dummy_request.params = dummy_request.POST = MultiDict()
    form = build_signup_form(dummy_request)

    # not raised
    with pytest.raises(Exception):
        with pytest.raises(ValidationError):
            field = mocker.Mock('field', data='oswald2')
            validate_email_uniqueness(form, field)


def test_validate_email_uniqueness_with_existing_email(
        mocker, users, dummy_request):
    user = users['oswald']
    # valid email
    user_email = user.emails.where(
        (UserEmail.activation_state == 'active') &
        (UserEmail.activation_token_expires_at >> None)).get()

    dummy_request.params = dummy_request.POST = MultiDict()
    form = build_signup_form(dummy_request)

    with pytest.raises(ValidationError):
        field = mocker.Mock('field', data=user_email.email)
        validate_email_uniqueness(form, field)


def test_validate_email_uniqueness_with_pending_email(
        mocker, users, dummy_request):
    user = users['johnny']
    # pending email
    user_email = user.emails.where(
        (UserEmail.activation_state == 'pending') &
        (UserEmail.activation_token_expires_at >= datetime.utcnow())).get()

    dummy_request.params = dummy_request.POST = MultiDict()
    form = build_signup_form(dummy_request)

    with pytest.raises(ValidationError):
        field = mocker.Mock('field', data=user_email.email)
        validate_email_uniqueness(form, field)


def test_validate_email_uniqueness_with_pending_expired_email(
        mocker, users, dummy_request):
    user = users['henry']
    # pending && expired email
    user_email = user.emails.where(
        (UserEmail.activation_state == 'pending') &
        (UserEmail.activation_token_expires_at <= datetime.utcnow())).get()

    dummy_request.params = dummy_request.POST = MultiDict()
    form = build_signup_form(dummy_request)

    # not raised
    with pytest.raises(Exception):
        with pytest.raises(ValidationError):
            field = mocker.Mock('field', data=user_email.email)
            validate_email_uniqueness(form, field)


def test_validate_email_uniqueness_with_new_email(mocker, dummy_request):
    dummy_request.params = dummy_request.POST = MultiDict()
    form = build_signup_form(dummy_request)

    # not raised
    with pytest.raises(Exception):
        with pytest.raises(ValidationError):
            field = mocker.Mock('field', data='oswald.new@example.org')
            validate_email_uniqueness(form, field)


def test_username_availability_check(mocker, dummy_request):
    user = User(username='scrolliris')

    dummy_request.params = dummy_request.POST = MultiDict()
    form = build_signup_form(dummy_request)

    with pytest.raises(ValidationError):
        field = mocker.Mock('field', data=user.username)
        username_availability_check(form, field)
