import os

from pyramid.decorator import reify


# OS's environ handler (wrapper)
# This class has utilities to treat environment variables.
class Env():
    VALUES = ('development', 'test', 'production')

    def __init__(self):
        v = str(os.environ.get('ENV', None))
        self._value = v if v in self.VALUES else 'production'

    @classmethod
    def load_dotenv_vars(cls, dotenv_file=None):
        # loads .env
        if dotenv_file is None:
            dotenv_file = os.path.join(os.getcwd(), '.env')
        if os.path.isfile(dotenv_file):
            print('loading environment variables from .env')
            from dotenv import load_dotenv
            load_dotenv(dotenv_file)

        if os.environ.get('ENV', None) == 'test':  # maps test_
            from test import test_vars

            for v in test_vars():
                test_v = os.environ.get('TEST_' + v, None)
                if test_v is not None:
                    os.environ[v] = test_v

    def get(self, key, default=None):
        return os.environ.get(key, default)

    def set(self, key, value):
        os.environ[key] = value

    @reify
    def host(self):
        # TODO
        # get host and port from server section in ini as fallback
        return str(self.get('HOST', '0.0.0.0'))

    @reify
    def port(self):
        return int(self.get('PORT', 8080))

    @reify
    def value(self):
        return self._value

    @reify
    def name(self):
        return self.value + 'ing' if self.value == 'test' else self.value

    @reify
    def is_test(self):
        return self._value == 'test'

    @reify
    def is_production(self):
        return self._value == 'production'

    @reify
    def settings_mappings(self):
        return {
            # Note: these values are updated if exist but not empty
            'auth.secret': 'AUTH_SECRET',
            'token.secret': 'TOKEN_SECRET',
            'domain': 'DOMAIN',
            'mail.host': 'MAIL_HOST',
            'mail.port': 'MAIL_PORT',
            'mail.username': 'MAIL_USERNAME',
            'mail.password': 'MAIL_PASSWORD',
            'mail.sender': 'MAIL_SENDER',
            'session.secret': 'SESSION_SECRET',
            'session.key': 'SESSION_KEY',
            'session.url': 'SESSION_URL',
            'session.username': 'SESSION_USERNAME',
            'session.password': 'SESSION_PASSWORD',
            'session.cookie_domain': 'SESSION_COOKIE_DOMAIN',
            'queue.url': 'QUEUE_URL',
            'database.cardinal.url': 'DATABASE_CARDINAL_URL',
            'database.analysis.url': 'DATABASE_ANALYSIS_URL',
            'pyramid.csrf_trusted_origins': 'CSRF_TRUSTED_ORIGINS',
            'wsgi.url_scheme': 'WSGI_URL_SCHEME',
            'wsgi.auth_credentials': 'WSGI_AUTH_CREDENTIALS',
        }
