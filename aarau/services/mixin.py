"""ActivatorMixin for class implements IActivator interface.

Inherit this Mixin in service.
"""

from datetime import datetime

from aarau.models.user_email import UserEmail


class ActivatorMixin(object):
    def __init__(self, request):
        self.request = request
        self._user = None
        self._user_email = None
        self._activation_token = None

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, value):
        self._user = value

    @property
    def user_email(self):
        return self._user_email

    @user_email.setter
    def user_email(self, value):
        self._user_email = value

    @property
    def activation_token(self):
        return self._activation_token

    @activation_token.setter
    def activation_token(self, value):
        self._activation_token = value

    def has_token_expired(self):
        """Checks token expiration validity for activation."""
        return self.user_email.activation_token_expires_at < datetime.utcnow()

    # TODO: refactor :'(
    def assign(self, user=None, email=None, token=None):
        """Assigns appropriate objects; user, user_email and activation_token.

        It raises DoesNotExit error if user email related to token does not
        exist
        """
        if user:
            self.user = user

        if token:
            self.activation_token = token

        # request (for generate_activation_email)
        if self.user and self.activation_token is None:
            # user: signup request
            if email is None:
                self.user_email = UserEmail(email=self.user.email,
                                            user=self.user, type='primary')
                return
            # email: change email request
            self.user_email = UserEmail(email=email, type='normal')
            return

        # activation (for activate)
        if self.activation_token and email is None:
            # token, user: email activation (new email)
            if self.user:
                self.user_email = self.user.emails.where(
                    UserEmail.activation_state == 'pending',
                    UserEmail.activation_token == self.activation_token).get()
            # token: account activation (signup)
            else:
                self.user_email = UserEmail.select().where(
                    UserEmail.type == 'primary',
                    UserEmail.activation_state == 'pending',
                    UserEmail.activation_token == self.activation_token).get()

                # pylint: disable=no-member
                # user's activation_state also must be 'pending'
                if not self.user_email or \
                   self.user_email.user.activation_state != 'pending':
                    self.user_email = None
                    raise UserEmail.DoesNotExist
