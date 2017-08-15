"""Tasks package.
"""
import ssl

from pyramid_celery import celery_app as worker
from pyramid.threadlocal import get_current_registry

from aarau import get_settings


__all__ = ('worker')


def init_worker(settings={}):  # pylint: disable=dangerous-default-value
    """Initializes worker (app).
    """
    if not settings:
        # for celery worker process
        # see aarau/scripts/worker.py
        import os
        from pyramid.paster import get_appsettings
        from aarau import resolve_env_vars
        from aarau.env import Env
        env = Env()

        config_uri = '{0!s}/config/{1!s}.ini#aarau'.format(
            os.path.dirname(__file__) + '/../..', env.name)
        settings = get_appsettings(config_uri)
        settings = resolve_env_vars(settings)

    options = {  # duplicated for consistency
        'broker_url': settings['queue.url'],
    }
    worker.conf.update(**options)
    return worker


worker = init_worker(get_settings())  # noqa pylint: disable=invalid-name


def blank_request():
    """Returns blank request object.
    """
    from aarau.request import CustomRequest

    # The variables wsgi.url_scheme, HTTP_HOST and SCRIPT_NAME
    # will be filled from pseudo base_url.
    request = CustomRequest.blank('/', base_url=None)
    request.registry = get_current_registry()
    return request


def includeme(config):
    """Initializes the celery task worker.

    Activate this setup using ``config.include('aarau.tasks')``.
    """
    # this makes request.task available for use in Pyramid
    config.add_request_method(
        lambda r: worker,
        'worker',
        reify=True
    )
