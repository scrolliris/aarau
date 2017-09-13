"""User account activation service.
"""

from aarau.services.mixin import ActivatorMixin
from aarau.tasks.send_email import send_account_activation_email


class AccountActivator(ActivatorMixin):
    """Service object for user account activation (signup).
    """

    def invoke(self):
        """Saves appropriate objects (user and user email).

        This method sends email for signup activation to new user, as side
        effect.
        """
        with self.request.db.cardinal.atomic():
            # self.user is not saved yet
            self.user.save()

            self.user_email.user = self.user
            self.user_email.save()

            self.user_email.generate_activation_token(expiration=3600)
            self.user_email.save()

            send_account_activation_email.delay(self.user_email.id)

    def activate(self):
        """Activates user using activation token.
        """
        with self.request.db.cardinal.atomic():
            result = self.user_email.activate(self.activation_token)

            self.user = self.user_email.user
            self.user.activation_state = 'active'
            self.user.save()
            return result
