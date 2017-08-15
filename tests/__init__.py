"""The testing package.
"""


def test_vars():
    """Returns env var names to update in testing.

    These values are updated with values prefixed as `TEST_`.
    See .env.sample.
    """
    return [
        'DOMAIN',
        'ENV',
        # application
        'DATABASE_URL',
        'QUEUE_URL',
        'CACHE_URL',
        'CSRF_TRUSTED_ORIGINS',
        # mailer
        'MAIL_HOST',
        'MAIL_PORT',
        'MAIL_USERNAME',
        'MAIL_PASSWORD',
        'MAIL_SENDER',
        'MAILER_TYPE',
        'MAILER_URL',
        'MAILER_DOMAIN',
        'MAILER_API_KEY',
        # activation
        'TOKEN_SECRET',
        # authentication
        'AUTH_SECRET',
        # session
        'SESSION_SECRET',
        'SESSION_KEY',
        'SESSION_URL',
        'SESSION_USERNAME',
        'SESSION_PASSWORD',
        'SESSION_COOKIE_DOMAIN',
        # datastore
        'TEST_DATASTORE_EMULATOR_HOST',
        'TEST_DATASTORE_PROJECT_ID',
    ]
