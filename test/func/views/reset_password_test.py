# pylint: disable=unused-argument
"""Test reset password view actions.
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


def test_reset_password_with_valid_email(  # pylint: disable=invalid-name
        users, login_as, dummy_app, mailbox):
    """Test password reset functionality.
    """
    user = users['oswald']
    res = dummy_app.get('/password/reset', status=200)
    res.charset = None
    form = res.forms['reset_password_request']
    form['email'] = user.email
    res = form.submit('submit', value='Request')

    assert '302 Found' == res.status
    assert 'http://example.org/password/reset' == res.location

    res = res.follow(status=200)
    res.charset = None
    # FIXME: locale
    assert 'reset_password.request.success' \
           '' in res.html.select_one('div.message')
    assert 'Reset password' in res.html.select_one('h4.header')

    message = mailbox.sent_messages[0]
    assert [user.email] == message.recipients
    assert 'Test <noreply@example.org>' == message.sender
    assert 'Reset your password' in message.subject
    assert 'To set a new password, just follow the link below' in message.body

    user.refresh()
    assert user.reset_password_token in message.body
