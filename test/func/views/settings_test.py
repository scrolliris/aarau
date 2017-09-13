# pylint: disable=unused-argument,invalid-name
"""Settings view functionality tests.
"""
import pytest


@pytest.fixture(autouse=True)
def setup(request, config, mailbox):
    """Setup.
    """
    mailbox.clean()

    # eager task (emulation)
    from aarau.tasks import worker
    worker.conf.update(task_always_eager=True)

    def teardown():
        """Teardown.
        """
        worker.conf.update(task_always_eager=False)
        mailbox.clean()

    request.addfinalizer(teardown)


def test_settings(users, login_as, dummy_app):
    """Test default (account) view.
    """
    user = users['oswald']
    with login_as(user):
        res = dummy_app.get('/settings', status=200)
        assert b'Account' in res.body


def test_settings_account_with_empty_params(users, login_as, dummy_app):
    """Test account view.
    """
    user = users['oswald']
    with login_as(user):
        res = dummy_app.get('/settings/account', status=200)
        assert b'Account' in res.body


def test_settings_email_with_empty_params(users, login_as, dummy_app):
    """Test email view.
    """
    user = users['oswald']
    with login_as(user):
        res = dummy_app.get('/settings/email', status=200)
        assert b'Email' in res.body


@pytest.mark.parametrize('params', [
    {},  # missing
    {'csrf_token': '12345'},  # invalid
])
def test_settings_email_with_invalid_csrf(users, login_as, params, dummy_app):
    """Test email view with invalid csrf token.
    """
    user = users['oswald']
    with login_as(user):
        params['new_email'] = user.email
        params['submit'] = '1'
        res = dummy_app.post('/settings/email', params=params, status=400)

        assert 'text/plain' == res.content_type
        assert b'400 Bad CSRF Token' in res.body


def test_settings_email_with_pending_email(users, login_as, dummy_app):
    """Test email saving if user has pending email.
    """
    from aarau.models.user_email import UserEmail

    user = users['henry']
    with login_as(user):
        user_email = user.emails.where(  # pending
            UserEmail.type == 'normal',
            UserEmail.activation_state == 'pending').get()

        res = dummy_app.get('/settings/email', status=200)
        res.charset = None
        token = res.html.select_one('input[name=csrf_token]')['value']
        params = {
            'csrf_token': token,
            'new_email': user_email,
            'submit': '1',
        }

        res = dummy_app.post('/settings/email', params=params, status=302)
        assert 'http://example.org/settings/email' == res.location
        res = res.follow(status=200)
        assert '200 OK' == res.status
        # FIXME: locale
        res.charset = None
        assert ('settings.email.addition.pending'
                '') in res.html.select_one('.warning.message')


def test_settings_email_with_invalid_email(users, login_as, dummy_app):
    """Test email saving with invalid email input.
    """
    from aarau.models.user_email import UserEmail

    user = users['oswald']
    with login_as(user):
        res = dummy_app.get('/settings/email', status=200)
        res.charset = None
        token = res.html.select_one('input[name=csrf_token]')['value']
        params = {
            'csrf_token': token,
            'new_email': 'invalid',
            'submit': '1',
        }

        res = dummy_app.post('/settings/email', params=params, status=200)
        assert '200 OK' == res.status
        # FIXME: locale
        res.charset = None
        assert ('settings.email.addition.failure'
                '') in res.html.select_one('.error.message')

        user_emails = user.emails.order_by(
            UserEmail.type.asc(), UserEmail.id.asc())
        assert [  # does not contain any change
            'oswald@example.org', 'oswald.private@example.org'
        ] == [ue.email for ue in user_emails]


def test_settings_email_with_valid_email(users, login_as, dummy_app):
    """Test email saving.
    """
    from aarau.models.user_email import UserEmail

    user = users['oswald']
    with login_as(user):
        res = dummy_app.get('/settings/email', status=200)
        res.charset = None
        token = res.html.select_one('input[name=csrf_token]')['value']
        params = {
            'csrf_token': token,
            'new_email': 'oswald.new@example.org',
            'submit': '1',
        }

        res = dummy_app.post('/settings/email', params=params, status=302)
        res = res.follow(status=200)
        assert '200 OK' == res.status
        # FIXME: locale
        res.charset = None
        assert ('settings.email.addition.success'
                '') in res.html.select_one('.success.message')

        user_emails = user.emails.order_by(
            UserEmail.type.asc(), UserEmail.id.asc())
        assert [  # does contain new email
            'oswald@example.org', 'oswald.private@example.org',
            'oswald.new@example.org'] == [ue.email for ue in user_emails]
        assert ['oswald.new@example.org'] == \
            [user_email.email for user_email in user_emails
             if user_email.activation_state == 'pending']


def test_settings_email_activate_with_expired_token(
        users, login_as, dummy_app):
    """Test email activation view with expired token.
    """
    from datetime import datetime
    from aarau.models.user_email import UserEmail

    user = users['henry']
    with login_as(user):
        user_email = users['henry'].emails.where(  # expired
            UserEmail.type == 'normal',
            UserEmail.activation_state == 'pending',
            UserEmail.activation_token_expires_at < datetime.utcnow()).get()
        assert 'pending' == user_email.activation_state

        params = {'token': user_email.activation_token}
        url = '/settings/email/confirm/{0:s}'.format(params['token'])
        res = dummy_app.get(url, status=302)
        res = res.follow(status=200)

        assert '200 OK' == res.status
        # FIXME: locale
        res.charset = None
        assert ('settings.email.confirmation.expired'
                '') in res.html.select_one('.error.message')


def test_settings_email_activate_with_unexpected_error(
        monkeypatch, users, login_as, dummy_app):
    """Test email activation view with error.
    """
    from aarau.models.user_email import UserEmail

    user = users['weenie']
    with login_as(user):
        user_email = users['weenie'].emails.where(
            UserEmail.type == 'normal',
            UserEmail.activation_state == 'pending').get()

        params = {'token': user_email.activation_token}
        url = '/settings/email/confirm/{0:s}'.format(params['token'])

        # simurate unexpected error (like configuration error)
        from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

        def mock_init(self, *args, **kwargs):
            return None

        monkeypatch.setattr(Serializer, '__init__', mock_init)

        res = dummy_app.get(url, status=302)
        res = res.follow(status=200)

        assert '200 OK' == res.status
        # FIXME: locale
        res.charset = None
        assert ('settings.email.confirmation.failure'
                '') in res.html.select_one('.error.message')


def test_settings_email_activate_with_valid_token(users, login_as, dummy_app):
    """Test email activation.
    """
    from aarau.models.user_email import UserEmail

    user = users['weenie']
    with login_as(user):
        user_email = user.emails.where(
            UserEmail.type == 'normal',
            UserEmail.activation_state == 'pending').get()

        params = {'token': user_email.activation_token}
        url = '/settings/email/confirm/{0:s}'.format(params['token'])

        res = dummy_app.get(url, status=302)
        res = res.follow(status=200)

        assert '200 OK' == res.status
        # FIXME: locale
        res.charset = None
        assert ('settings.email.confirmation.success'
                '') in res.html.select_one('.success.message')

        user_email.refresh()
        assert 'active' == user_email.activation_state


@pytest.mark.parametrize('user_email', [
    'invalid',  # invalid
    'henry@example.org',  # henry's primary
])
def test_settings_email_delete_with_invalid_email(
        users, login_as, user_email, dummy_app):
    """Test email deletion with invalid email input.
    """
    user = users['henry']
    with login_as(user):
        res = dummy_app.get('/settings/email', status=200)
        res.charset = None
        token = res.html.select_one('input[name=csrf_token]')['value']
        params = {
            'csrf_token': token,
            'email': user_email,
            'submit': '1',
        }

        res = dummy_app.post(
            '/settings/email/delete', params=params, status=302)
        res = res.follow(status=200)

        assert '200 OK' == res.status
        # FIXME: locale
        res.charset = None
        assert ('settings.email.deletion.failure'
                '') in res.html.select_one('.error.message')


def test_settings_email_delete_with_valid_email(
        users, login_as, dummy_app):
    """Test email deletion.
    """
    from aarau.models.user_email import UserEmail

    user = users['weenie']
    with login_as(user):
        user_email = user.emails.where(
            UserEmail.type == 'normal',
            UserEmail.activation_state == 'pending').get()

        res = dummy_app.get('/settings/email', status=200)
        res.charset = None
        token = res.html.select_one('input[name=csrf_token]')['value']
        params = {
            'csrf_token': token,
            'email': user_email.email,
            'submit': '1',
        }

        res = dummy_app.post(
            '/settings/email/delete', params=params, status=302)
        res = res.follow(status=200)

        assert '200 OK' == res.status
        # FIXME: locale
        res.charset = None
        assert ('settings.email.deletion.success'
                '') in res.html.select_one('.success.message')

        # pylint: disable=no-member
        with pytest.raises(UserEmail.DoesNotExist):
            assert user_email.refresh()


# TODO test_settings_email_change


def test_settings_password_with_empty_params(users, login_as, dummy_app):
    """Test password view.
    """
    user = users['oswald']
    with login_as(user):
        res = dummy_app.get('/settings/password', status=200)
        assert b'Password' in res.body


@pytest.mark.parametrize('params', [
    {},  # missing
    {'csrf_token': '12345'},  # invalid
])
def test_settings_password_with_invalid_csrf(
        users, login_as, params, dummy_app):
    """Test password updating with invalid csrf token.
    """
    user = users['oswald']
    with login_as(user):
        params['current_password'] = '0PlayingPiano'
        params['new_password'] = 'wrong'
        params['new_password_confirmation'] = 'wrong'
        params['submit'] = '1'
        res = dummy_app.post('/settings/password', params=params, status=400)

        assert 'text/plain' == res.content_type
        assert b'400 Bad CSRF Token' in res.body


def test_settings_password_with_validation_errors(
        users, login_as, dummy_app):
    """Test password saving validation errors.
    """
    user = users['oswald']
    with login_as(user):
        res = dummy_app.get('/settings/password', status=200)
        res.charset = None
        form = res.forms['change_password']
        form['current_password'] = '0PlayingPiano'
        form['new_password'] = 'wrong'
        form['new_password_confirmation'] = 'wrong'
        res = form.submit('submit', value='Change')

        assert '200 OK' == res.status
        # FIXME: locale
        res.charset = None
        assert ('settings.password.change.failure'
                '') in res.html.select_one('.error.message')
        assert 'Field must be between 6 and 32 characters long.' in \
            res.html.form.text
        assert 'Password' in res.html.select_one('.header > h6')


def test_settings_password_with_valid_credentials(
        users, login_as, dummy_app):
    """Test password saving with invalid credentials.
    """
    user = users['oswald']
    with login_as(user):
        res = dummy_app.get('/settings/password', status=200)
        res.charset = None
        form = res.forms['change_password']
        form['current_password'] = '0PlayingPiano'
        form['new_password'] = 'NewpaSsw0rd'
        form['new_password_confirmation'] = 'NewpaSsw0rd'
        res = form.submit('submit', value='Change')

        assert '302 Found' == res.status
        assert 'http://example.org/settings/password' == res.location

        res = res.follow(status=200)
        # FIXME: locale
        res.charset = None
        assert ('settings.password.change.success'
                '') in res.html.select_one('.success.message')
        assert 'Password' in res.html.select_one('.header > h6')
