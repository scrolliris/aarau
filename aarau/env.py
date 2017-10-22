import os

from pyramid.decorator import reify


def load_dotenv_vars(dotenv_file=None):
    # loads .env
    if dotenv_file is None:
        dotenv_file = os.path.join(os.getcwd(), '.env')
    if os.path.isfile(dotenv_file):
        print('loading environment variables from .env')
        from dotenv import load_dotenv
        load_dotenv(dotenv_file)

    # update vars using prefix such as {TEST_|DEVELOPMENT_|PRODUCTION_}
    for _, v in Env.settings_mappings().items():
        prefix = '{}_'.format(Env.env_name().upper())
        env_v = os.environ.get(prefix + v, None)
        if env_v is not None:
            os.environ[v] = env_v


class Env():
    """The wrapper of `os.environ` for application."""

    VALUES = ('development', 'test', 'production')

    def __init__(self):
        self._value = self.__class__.env_name()

    @classmethod
    def env_name(cls):
        v = str(os.environ.get('ENV', None))
        return v if v in cls.VALUES else 'production'

    @staticmethod
    def settings_mappings():
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
            'mailer.type': 'MAILER_TYPE',
            'mailer.url': 'MAILER_URL',
            'mailer.domain': 'MAILER_DOMAIN',
            'mailer.api_key': 'MAILER_API_KEY',
            'session.secret': 'SESSION_SECRET',
            'session.key': 'SESSION_KEY',
            'session.url': 'SESSION_URL',
            'session.username': 'SESSION_USERNAME',
            'session.password': 'SESSION_PASSWORD',
            'session.cookie_domain': 'SESSION_COOKIE_DOMAIN',
            'queue.url': 'QUEUE_URL',
            'cache.url': 'CACHE_URL',
            'font.typekit_id': 'FONT_TYPEKIT_ID',
            'database.cardinal.url': 'DATABASE_CARDINAL_URL',
            'database.analysis.url': 'DATABASE_ANALYSIS_URL',
            'pyramid.csrf_trusted_origins': 'CSRF_TRUSTED_ORIGINS',
            'wsgi.url_scheme': 'WSGI_URL_SCHEME',
            'wsgi.auth_credentials': 'WSGI_AUTH_CREDENTIALS',
            'datastore.emulator_host': 'DATASTORE_EMULATOR_HOST',
            'datastore.project_id': 'DATASTORE_PROJECT_ID',
            'storage.bucket_host': 'STORAGE_BUCKET_HOST',
            'storage.bucket_name': 'STORAGE_BUCKET_NAME',
            'storage.bucket_path': 'STORAGE_BUCKET_PATH',
            # deployment
            'google_cloud.project': 'GOOGLE_CLOUD_PROJECT',
        }

    def get(self, key, default=None):  # pylint: disable=no-self-use
        return os.environ.get(key, default)

    def set(self, key, value):  # pylint: disable=no-self-use
        os.environ[key] = value

    @reify
    def host(self):
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
