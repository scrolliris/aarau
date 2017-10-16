import pytest

from webob.multidict import MultiDict
from aarau.views.signup.form import (
    build_signup_form,
    SignupForm,
)


@pytest.fixture(autouse=True)
def setup(request, config):
    pass

    def teardown():
        pass

    request.addfinalizer(teardown)


def test_build_signup_form(dummy_request):
    dummy_request.params = dummy_request.POST = MultiDict()
    form = build_signup_form(dummy_request)
    assert isinstance(form, SignupForm)


def test_validate_email_with_existing_email(mocker, users, dummy_request):
    from wtforms import ValidationError
    from aarau.models import UserEmail

    user = users['oswald']
    # valid email
    user_email = user.emails.where(
        (UserEmail.activation_state == 'active') &
        (UserEmail.activation_token_expires_at >> None)).get()

    dummy_request.params = dummy_request.POST = MultiDict()
    form = build_signup_form(dummy_request)

    with pytest.raises(ValidationError):
        field = mocker.Mock('field', data=user_email.email)
        form.validate_email(field)


def test_validate_email_with_pending_email(mocker, users, dummy_request):
    from datetime import datetime
    from wtforms import ValidationError
    from aarau.models import UserEmail

    user = users['johnny']
    # pending email
    user_email = user.emails.where(
        (UserEmail.activation_state == 'pending') &
        (UserEmail.activation_token_expires_at >= datetime.utcnow())).get()

    dummy_request.params = dummy_request.POST = MultiDict()
    form = build_signup_form(dummy_request)

    with pytest.raises(ValidationError):
        field = mocker.Mock('field', data=user_email.email)
        form.validate_email(field)


def test_validate_email_with_pending_expired_email(
        mocker, users, dummy_request):
    from datetime import datetime
    from wtforms import ValidationError
    from aarau.models import UserEmail

    user = users['henry']
    # pending && expired email
    user_email = user.emails.where(
        (UserEmail.activation_state == 'pending') &
        (UserEmail.activation_token_expires_at <= datetime.utcnow())).get()

    dummy_request.params = dummy_request.POST = MultiDict()
    form = build_signup_form(dummy_request)

    with pytest.raises(Exception):
        with pytest.raises(ValidationError):
            field = mocker.Mock('field', data=user_email.email)
            form.validate_email(field)


def test_validate_email_with_new_email(mocker, users, dummy_request):
    from wtforms import ValidationError

    dummy_request.params = dummy_request.POST = MultiDict()
    form = build_signup_form(dummy_request)

    with pytest.raises(Exception):
        with pytest.raises(ValidationError):
            field = mocker.Mock('field', data='oswald.new@example.org')
            form.validate_email(field)
