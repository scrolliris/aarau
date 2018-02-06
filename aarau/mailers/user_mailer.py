from contextlib import contextmanager
import hashlib
import time
import requests

from pyramid.renderers import render
from pyramid_mailer import get_mailer
from pyramid_mailer.message import Message as BaseMessage

from aarau.env import Env

__all__ = ('UserMailer')


class Message(BaseMessage):
    def __init__(self, **kw):
        from .. import get_settings
        settings = get_settings()
        kw['sender'] = settings['mail.sender']
        super().__init__(**kw)


class Mailer(object):
    def __init__(self, mailer, message):
        self.mailer = mailer
        self.message = message

    def deliver(self):
        env = Env()
        typ = env.get('MAILER_TYPE', 'smtp')

        if typ == 'smtp':
            self.mailer.send_immediately(self.message, fail_silently=False)

        if typ == 'http':  # use `HTTP` api
            url = env.get('MAILER_URL', '{}').format(
                env.get('MAILER_DOMAIN', ''))
            auth = ('api', env.get('MAILER_API_KEY', ''))
            data = {
                'from': self.message.sender,
                'to': self.message.recipients,
                'subject': self.message.subject,
                'text': self.message.body,
            }
            res = requests.post(url, auth=auth, data=data)
            res.raise_for_status()


@contextmanager
def mail_to(user_email):
    if user_email is None or user_email.email is None:
        raise ValueError('UserMailer needs a valid user as recipient :(')
    yield [user_email.email]


class UserMailer(object):
    def __init__(self, request):
        self.request = request
        self.template = '../templates/user_mailer/{}.text.mako'

    @staticmethod
    def generate_hash_ref(length=9):
        hash_ref = hashlib.sha256()
        hash_ref.update(str(time.time()).encode('utf8'))
        ref = hash_ref.hexdigest()
        ref_length = len(ref)
        return ref[:(ref_length if length > ref_length else length)]

    def reset_password_email(self, user=None):
        with mail_to(user) as recipients:
            url = self.request.route_url('reset_password',
                                         token=user.reset_password_token)
            body = render(self.template.format('reset_password_email'), {
                'url': url,
                'ref': self.__class__.generate_hash_ref(),
            })
            message = Message(subject='Reset your password',
                              recipients=recipients,
                              body=body)

        return Mailer(get_mailer(self.request), message)

    def account_activation_email(self, user_email=None):
        with mail_to(user_email) as recipients:
            url = self.request.route_url('signup.activate',
                                         token=user_email.activation_token)
            body = render(self.template.format('account_activation_email'), {
                'url': url,
                'ref': self.__class__.generate_hash_ref(),
            })
            message = Message(subject='Activate your account',
                              recipients=recipients,
                              body=body)

        return Mailer(get_mailer(self.request), message)

    def email_activation_email(self, user_email=None):
        with mail_to(user_email) as recipients:
            url = self.request.route_url('carrell.settings.email_activate',
                                         token=user_email.activation_token)
            body = render(self.template.format('email_activation_email'), {
                'url': url,
                'ref': self.__class__.generate_hash_ref(),
            })
            message = Message(subject='Confirm your new email address',
                              recipients=recipients,
                              body=body)

        return Mailer(get_mailer(self.request), message)
