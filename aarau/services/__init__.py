from aarau.services.interface import IActivator, IReplicator
from aarau.services.account_activator import AccountActivator
from aarau.services.site_replicator import SiteReplicator
from aarau.services.user_email_activator import UserEmailActivator

__all__ = (
    'AccountActivator',
    'UserEmailActivator',
    'SiteReplicator',
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


def replicator_factory(replication_obj='site'):
    """Returns replicator service factory method."""
    def _replicator_factory(_, req):
        if replication_obj == 'site':
            return SiteReplicator(req)
        return None

    return _replicator_factory


def includeme(config):
    """Initializes service objects.

    Activate this setup using ``config.include('aarau.services')``.
    """
    # activator services
    for name in ('user_email', 'account',):
        config.register_service_factory(activator_factory(name),
                                        iface=IActivator, name=name)

    # replicator services
    for name in ('site',):
        config.register_service_factory(replicator_factory(name),
                                        iface=IReplicator, name=name)
