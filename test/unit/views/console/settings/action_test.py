import pytest
from webob.multidict import MultiDict


@pytest.fixture(autouse=True)
def setup(request, config, mailer_outbox):  # pylint: disable=unused-argument
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


def assert_user_email_forms(user_emails, email_forms):
    from aarau.views.console.settings.form import (
        FailureForm,
        ChangeEmailForm,
        DeleteEmailForm,
    )
    for ue in user_emails:
        form_dict = email_forms[ue.id]
        if ue.type == 'primary':
            assert isinstance(form_dict['change'], FailureForm)
            assert isinstance(form_dict['delete'], FailureForm)
        elif ue.activation_state == 'pending':
            assert isinstance(form_dict['change'], FailureForm)
            assert isinstance(form_dict['delete'], DeleteEmailForm)
        else:
            assert isinstance(form_dict['change'], ChangeEmailForm)
            assert isinstance(form_dict['delete'], DeleteEmailForm)


def test_settings_account(users, dummy_request):
    from aarau.views.console.settings.action import settings_account

    dummy_request.subdomain = 'console'
    dummy_request.user = users['oswald']
    res = settings_account(dummy_request)

    assert {} == res


def test_settings_email_with_empty_params(users, dummy_request):
    from aarau.views.console.settings.action import settings_email
    from aarau.views.console.settings.form import NewEmailForm

    user = users['oswald']

    dummy_request.subdomain = 'console'
    dummy_request.user = user
    dummy_request.POST = MultiDict({})
    res = settings_email(dummy_request)

    assert isinstance(res['form'], NewEmailForm)
    assert user.emails.count() == res['user_emails'].count()
    assert_user_email_forms(res['user_emails'], res['email_forms'])
    assert not dummy_request.session.peek_flash()


def test_settings_email_with_missing_csrf(users, dummy_request):
    from aarau.views.console.settings.action import settings_email
    from aarau.views.console.settings.form import NewEmailForm

    user = users['oswald']
    new_email = 'new.oswald@example.org'

    dummy_request.subdomain = 'console'
    dummy_request.user = user
    dummy_request.POST = MultiDict({
        # 'csrf_token': '',
        'new_email': new_email,
        'submit': '1',
    })
    res = settings_email(dummy_request)

    assert isinstance(res['form'], NewEmailForm)
    assert new_email not in [e.email for e in user.emails]
    assert new_email not in [e.email for e in res['user_emails']]
    assert user.emails.count() == res['user_emails'].count()
    assert_user_email_forms(res['user_emails'], res['email_forms'])
    assert {'csrf_token': ['Invalid CSRF']} == res['form'].errors
    assert dummy_request.session.peek_flash('failure')


def test_settings_email_with_invalid_csrf(users, dummy_request):
    from aarau.views.console.settings.action import settings_email
    from aarau.views.console.settings.form import NewEmailForm

    user = users['oswald']
    new_email = 'new.oswald@example.org'

    dummy_request.subdomain = 'console'
    dummy_request.user = user
    dummy_request.POST = MultiDict({
        'csrf_token': 'invalid',
        'new_email': new_email,
        'submit': '1',
    })
    res = settings_email(dummy_request)

    assert isinstance(res['form'], NewEmailForm)
    assert new_email not in [e.email for e in user.emails]
    assert new_email not in [e.email for e in res['user_emails']]
    assert user.emails.count() == res['user_emails'].count()
    assert_user_email_forms(res['user_emails'], res['email_forms'])
    assert {'csrf_token': ['Invalid CSRF']} == res['form'].errors
    assert dummy_request.session.peek_flash('failure')


def test_settings_email_with_pending_email(
        users, dummy_request):
    from aarau.views.console.settings.action import settings_email

    user = users['henry']

    dummy_request.subdomain = 'console'
    dummy_request.user = user
    dummy_request.POST = MultiDict({
        'csrf_token': dummy_request.session.get_csrf_token(),
        'new_email': 'henry.new@example.org',
        'submit': '1',
    })
    res = settings_email(dummy_request)

    assert dict != type(res)
    assert dummy_request.session.peek_flash('warning')
    assert '302 Found' == res.status
    assert '/settings/email' == res.location


def test_settings_email_with_invalid_email(users, dummy_request):
    from aarau.views.console.settings.action import settings_email
    from aarau.views.console.settings.form import NewEmailForm

    user = users['oswald']

    dummy_request.subdomain = 'console'
    dummy_request.user = user
    dummy_request.POST = MultiDict({
        'csrf_token': dummy_request.session.get_csrf_token(),
        'new_email': 'invalid',
        'submit': '1',
    })
    res = settings_email(dummy_request)

    assert isinstance(res['form'], NewEmailForm)
    assert [  # does not contain any change in res
        'oswald@example.org', 'oswald.private@example.org'
    ] == [ue.email for ue in res['user_emails']]
    assert_user_email_forms(res['user_emails'], res['email_forms'])
    assert {'new_email': ['Invalid email address.']} == res['form'].errors
    assert dummy_request.session.peek_flash('failure')


def test_settings_email_with_valid_email(users, dummy_request):
    from aarau.views.console.settings.action import settings_email

    dummy_request.subdomain = 'console'
    dummy_request.user = users['oswald']
    dummy_request.POST = MultiDict({
        'csrf_token': dummy_request.session.get_csrf_token(),
        'new_email': 'oswald.new@example.org',
        'submit': '1',
    })
    assert 2 == users['oswald'].emails.count()

    res = settings_email(dummy_request)

    assert dict != type(res)
    assert dummy_request.session.peek_flash('success')
    assert '302 Found' == res.status
    assert '/settings/email' == res.location


def test_settings_email_activate_with_invalid_token(
        users, dummy_request):
    from pyramid.httpexceptions import HTTPNotFound
    from aarau.views.console.settings.action import settings_email_activate

    dummy_request.subdomain = 'console'
    dummy_request.user = users['oswald']
    dummy_request.matchdict = {
        'token': 'invalid'
    }
    with pytest.raises(HTTPNotFound):
        res = settings_email_activate(dummy_request)

        assert not dummy_request.session.peek_flash()
        assert '404 NotFound' == res.status


def test_settings_email_activate_with_expired_token(
        users, dummy_request):
    from aarau.views.console.settings.action import settings_email_activate
    from aarau.models.user_email import UserEmail

    user_email = users['henry'].emails.where(
        UserEmail.email == 'henry.expired@example.org').get()

    dummy_request.subdomain = 'console'
    dummy_request.user = users['henry']
    dummy_request.matchdict = {
        'token': user_email.activation_token
    }
    res = settings_email_activate(dummy_request)

    assert dummy_request.session.peek_flash('warning')
    assert '302 Found' == res.status
    assert '/settings/email' == res.location


def test_settings_email_activate_with_unexpected_error(
        users, dummy_request):
    from aarau.views.console.settings.action import settings_email_activate
    from aarau.models.user_email import UserEmail

    user_email = users['weenie'].emails.where(
        UserEmail.email == 'weenie.private@example.org').get()
    assert 'pending' == user_email.activation_state

    dummy_request.subdomain = 'console'
    dummy_request.user = users['weenie']
    dummy_request.matchdict = {
        'token': user_email.activation_token
    }

    try:
        from aarau import get_settings
        settings = get_settings()
        secret = settings['token.secret']
        settings['token.secret'] = None  # emulate as not set

        res = settings_email_activate(dummy_request)

        assert dummy_request.session.peek_flash('failure')
        assert '302 Found' == res.status
        assert '/settings/email' == res.location
    finally:
        # restore for following tests
        settings['token.secret'] = secret


def test_settings_email_activate_with_valid_token(
        users, dummy_request):
    from aarau.views.console.settings.action import settings_email_activate
    from aarau.models.user_email import UserEmail

    user_email = users['weenie'].emails.where(
        UserEmail.email == 'weenie.private@example.org').get()
    assert 'pending' == user_email.activation_state

    dummy_request.subdomain = 'console'
    dummy_request.user = users['weenie']
    dummy_request.matchdict = {
        'token': user_email.activation_token
    }
    res = settings_email_activate(dummy_request)

    assert dummy_request.session.peek_flash('success')
    assert '302 Found' == res.status
    assert '/settings/email' == res.location


def test_settings_email_delete_with_primary_email(
        users, dummy_request):
    from aarau.views.console.settings.action import settings_email_delete
    from aarau.models.user_email import UserEmail

    user_email = users['weenie'].emails.where(
        UserEmail.type == 'primary').get()
    assert 'active' == user_email.activation_state

    dummy_request.subdomain = 'console'
    dummy_request.user = users['weenie']
    dummy_request.POST = dummy_request.params = MultiDict({
        'csrf_token': dummy_request.session.get_csrf_token(),
        'email': user_email.email,
        'submit': '1',
    })
    res = settings_email_delete(dummy_request)

    assert '302 Found' == res.status
    assert '/settings/email' == res.location


def test_settings_email_delete_with_valid_email(
        users, dummy_request):
    from aarau.views.console.settings.action import settings_email_delete
    from aarau.models.user_email import UserEmail

    user_email = users['henry'].emails.where(
        UserEmail.email == 'henry.expired@example.org').get()
    assert 'pending' == user_email.activation_state
    assert 'normal' == user_email.type

    dummy_request.subdomain = 'console'
    dummy_request.user = users['henry']
    dummy_request.POST = dummy_request.params = MultiDict({
        'csrf_token': dummy_request.session.get_csrf_token(),
        'email': user_email.email,
        'submit': '1',
    })
    res = settings_email_delete(dummy_request)

    assert '302 Found' == res.status
    assert '/settings/email' == res.location


def test_settings_email_change_with_missing_csrf(
        users, dummy_request):
    from aarau.views.console.settings.action import settings_email_change
    from aarau.models.user_email import UserEmail

    user = users['oswald']
    alt_user_email = user.emails.where(
        UserEmail.email != user.email).get()

    dummy_request.subdomain = 'console'
    dummy_request.user = user
    dummy_request.POST = dummy_request.params = MultiDict({
        # 'csrf_token': '',
        'email': alt_user_email.email,
        'submit': '1',
    })
    res = settings_email_change(dummy_request)

    assert '302 Found' == res.status
    assert '/settings/email' == res.location
    assert dummy_request.session.peek_flash('failure')


def test_settings_email_change_with_invalid_csrf(
        users, dummy_request):
    from aarau.views.console.settings.action import settings_email_change
    from aarau.models.user_email import UserEmail

    user = users['oswald']
    alt_user_email = user.emails.where(
        UserEmail.email != user.email).get()

    dummy_request.subdomain = 'console'
    dummy_request.user = user
    dummy_request.POST = dummy_request.params = MultiDict({
        'csrf_token': 'invalid',
        'email': alt_user_email.email,
        'submit': '1',
    })
    res = settings_email_change(dummy_request)

    assert '302 Found' == res.status
    assert '/settings/email' == res.location
    assert dummy_request.session.peek_flash('failure')


def test_settings_email_change_with_current_primary_email(
        users, dummy_request):
    from aarau.views.console.settings.action import settings_email_change

    user = users['oswald']

    dummy_request.subdomain = 'console'
    dummy_request.user = user
    dummy_request.POST = dummy_request.params = MultiDict({
        'csrf_token': dummy_request.session.get_csrf_token(),
        'email': user.email,  # (current) primary email
        'submit': '1',
    })
    res = settings_email_change(dummy_request)

    assert '302 Found' == res.status
    assert '/settings/email' == res.location
    assert dummy_request.session.peek_flash('failure')


def test_settings_email_change(users, dummy_request):
    from aarau.views.console.settings.action import settings_email_change
    from aarau.models.user_email import UserEmail

    user = users['oswald']
    alt_user_email = user.emails.where(
        UserEmail.email != user.email).get()

    dummy_request.subdomain = 'console'
    dummy_request.user = user
    dummy_request.POST = dummy_request.params = MultiDict({
        'csrf_token': dummy_request.session.get_csrf_token(),
        'email': alt_user_email.email,
        'submit': '1',
    })
    res = settings_email_change(dummy_request)

    assert '302 Found' == res.status
    assert '/settings/email' == res.location
    assert dummy_request.session.peek_flash('success')


def test_settings_password_with_empty_params(users, dummy_request):
    from aarau.views.console.settings.action import settings_password
    from aarau.views.console.settings.form import ChangePasswordForm

    dummy_request.subdomain = 'console'
    dummy_request.user = users['oswald']
    dummy_request.POST = MultiDict({})
    res = settings_password(dummy_request)

    assert isinstance(res['form'], ChangePasswordForm)


def test_settings_password_with_invalid_csrf(users, dummy_request):
    from aarau.views.console.settings.action import settings_password
    from aarau.views.console.settings.form import ChangePasswordForm

    dummy_request.subdomain = 'console'
    dummy_request.user = users['oswald']
    dummy_request.POST = MultiDict({
        'csrf_token': 'invalid',
        'current_password': '0PlayingPiano',
        'new_password': 'NewpaSsw0rd',
        'new_password_confirmation': 'NewpaSsw0rd',
        'submit': '1',
    })
    res = settings_password(dummy_request)

    assert isinstance(res['form'], ChangePasswordForm)
    assert {'csrf_token': ['Invalid CSRF']} == res['form'].errors
    assert dummy_request.session.peek_flash('failure')


def test_settings_password_with_wrong_current_password(
        users, dummy_request):
    from aarau.views.console.settings.action import settings_password
    from aarau.views.console.settings.form import ChangePasswordForm

    dummy_request.subdomain = 'console'
    dummy_request.user = users['oswald']
    dummy_request.POST = MultiDict({
        'csrf_token': dummy_request.session.get_csrf_token(),
        'current_password': 'wrOng_passw0rd',
        'new_password': 'NewpaSsw0rd',
        'new_password_confirmation': 'NewpaSsw0rd',
        'submit': '1',
    })
    res = settings_password(dummy_request)

    assert isinstance(res['form'], ChangePasswordForm)
    assert {} == res['form'].errors
    assert dummy_request.session.peek_flash('failure')


def test_settings_password_with_invalid_new_password(
        users, dummy_request):
    from aarau.views.console.settings.action import settings_password
    from aarau.views.console.settings.form import ChangePasswordForm

    dummy_request.subdomain = 'console'
    dummy_request.user = users['oswald']
    dummy_request.POST = MultiDict({
        'submit': '1',
        'csrf_token': dummy_request.session.get_csrf_token(),
        'current_password': '0PlayingPiano',
        'new_password': 'Sh0rt',
        'new_password_confirmation': 'Sh0rt',
    })
    res = settings_password(dummy_request)

    assert isinstance(res['form'], ChangePasswordForm)
    assert {'new_password': [
        'Field must be between 8 and 32 characters long.',
    ]} == res['form'].errors
    assert dummy_request.session.peek_flash('failure')


def test_settings_password_with_invalid_new_password_confirmation(
        users, dummy_request):
    from aarau.views.console.settings.action import settings_password
    from aarau.views.console.settings.form import ChangePasswordForm

    dummy_request.subdomain = 'console'
    dummy_request.user = users['oswald']
    dummy_request.POST = MultiDict({
        'csrf_token': dummy_request.session.get_csrf_token(),
        'current_password': '0PlayingPiano',
        'new_password': 'NewpaSsw0rd',
        'new_password_confirmation': 'newpassword',
        'submit': '1',
    })
    res = settings_password(dummy_request)

    assert isinstance(res['form'], ChangePasswordForm)
    assert {'new_password_confirmation': [
        'Passwords must match',
    ]} == res['form'].errors
    assert dummy_request.session.peek_flash('failure')


def test_settings_password_with_valid_params(users, dummy_request):
    from aarau.views.console.settings.action import settings_password

    dummy_request.subdomain = 'console'
    dummy_request.user = users['oswald']
    dummy_request.POST = MultiDict({
        'csrf_token': dummy_request.session.get_csrf_token(),
        'current_password': '0PlayingPiano',
        'new_password': 'NewpaSsw0rd',
        'new_password_confirmation': 'NewpaSsw0rd',
        'submit': '1',
    })
    res = settings_password(dummy_request)

    assert '302 Found' == res.status
    assert '/settings/password' == res.location
    assert dummy_request.session.peek_flash('success')
