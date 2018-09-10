from aarau.services.interface import IActivator, IManager
from aarau.services.account_activator import AccountActivator
from aarau.services.credentials_manager import CredentialsManager
from aarau.services.user_email_activator import UserEmailActivator

__all__ = (
    'AccountActivator',
    'UserEmailActivator',
    'CredentialsManager',
)


def activator_factory(activation_type='user_email'):
    """Returns activator service factory method."""
    def _activator_factory(_, req):
        if activation_type == 'user_email':
            return UserEmailActivator(req)
        if activation_type == 'account':
            return AccountActivator(req)
        return None

    return _activator_factory


def manager_factory(manage_obj='site'):
    """Returns manager service factory method."""
    def _manager_factory(_, req):
        if manage_obj == 'credentials':
            return CredentialsManager(req)
        return None

    return _manager_factory


def includeme(config):
    """Initializes service objects.

    Activate this setup using ``config.include('aarau.services')``.
    """
    # activator services
    for name in ('user_email', 'account',):
        config.register_service_factory(activator_factory(name),
                                        iface=IActivator, name=name)

    # manager services
    for name in ('credentials',):
        config.register_service_factory(manager_factory(name),
                                        iface=IManager, name=name)
