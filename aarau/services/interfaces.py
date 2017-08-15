# pylint: disable=inherit-non-class,no-self-argument,no-method-argument
"""Interface classes as service object.
"""

from zope.interface import Attribute, Interface


class IActivator(Interface):
    """Interface as activator service
    """
    # pylint: disable=missing-docstring
    user = Attribute("""user object""")
    user_email = Attribute("""user_email obejct""")
    activation_token = Attribute("""user_email object's activation_token""")

    def assign(user=None, email=None, token=None):
        pass

    def activate():
        pass

    def invoke():
        pass

    def token_has_expired():
        pass


class IReplicator(Interface):
    """Interface as replicator service
    """
    # pylint: disable=missing-docstring
    obj = Attribute("""object""")

    def assign(obj=None):
        pass

    def replicate():
        pass

    def validate():
        pass

    def destroy():
        pass
