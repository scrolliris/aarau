""" UserEmail activation service
"""

from aarau.services.mixins import ActivatorMixin
from aarau.tasks.send_email import send_email_activation_email


class UserEmailActivator(ActivatorMixin):
    """ Service object for user email activation
    """

    def invoke(self):
        """ Saves appropriate object (user email)

        This method sends email for activation to user's new email address,
        as side effect.
        """
        with self.request.db.atomic():
            self.user_email.user = self.user
            # user_email must be saved once here to get id for token generation
            self.user_email.save()

            self.user_email.generate_activation_token(expiration=3600)
            self.user_email.save()

            send_email_activation_email.delay(self.user_email.id)

    def activate(self):
        """ Activates user email using activation token
        """
        return self.user_email.activate(self.activation_token)
