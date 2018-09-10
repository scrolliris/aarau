# pylint: disable=inherit-non-class,no-self-argument
from zope.interface import Attribute, Interface


class IActivator(Interface):
    user = Attribute("""user object""")
    user_email = Attribute("""user_email obejct""")
    activation_token = Attribute("""user_email object's activation_token""")

    def invoke(self):
        pass

    def token_has_expired(self):
        pass


class IManager(Interface):
    obj = Attribute("""object""")

    def sync(self):
        pass

    def validate(self):
        pass

    def destroy(self):
        pass
