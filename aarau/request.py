"""Request module.
"""

import re
import ipaddress

from pyramid.decorator import reify
from pyramid.request import Request

from aarau.env import Env
from aarau.models import db

__all__ = ('CustomRequest')

IPV4_ADDR = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
IPV6_ADDR = re.compile(r'[0-9a-f]+[0-9a-f:]+')

TRUSTED_NETWORKS = [ipaddress.ip_network(n) for n in [
    '127.0.0.1',       # localhost ipv4
    '::1',             # localhost ipv6
    '10.0.0.0/8',      # private ipv4 range
    '172.16.0.0/12',   # private ipv4 range
    '192.168.0.0/16',  # private ipv4 range
    'fc00::/7',        # private ipv6 range
]]

ASSET_PATH = re.compile(r'^\/?(assets|favicon\.ico|.*\.txt|.*\.png)')
HEALTH_CHECK_PATH = re.compile(r'^\/_ah\/health\/?$')


class CustomRequest(Request):
    """The custom request class has some utilities and callbacks.
    """
    def __init__(self, *args, **kwargs):
        env_dict = (args[0] or {})

        # self.environ is request env.
        # the `env` is os's environ handler (wrapper)
        self.env = Env()
        if self.env.is_production:
            env_dict = self._force_ssl(env_dict)
            env_dict = self.__class__.trim_port(env_dict)

        new_args = (env_dict, args[1:])

        # create base_url from pseudo values for tasks
        if 'base_url' in kwargs and kwargs['base_url'] is None:
            # pylint: disable=no-member
            base_url = '{0!s}://{1!s}:{2!s}'.format(
                self.settings.get('wsgi.url_scheme', 'https'),
                self.environ.get('HTTP_HOST', '127.0.0.1'),
                self.environ.get('HTTP_PORT', '8080')
            )
            if self.env.is_production:
                base_url = re.sub(':[0-9]+$', '', base_url)

            kwargs['base_url'] = base_url

        super().__init__(*new_args, **kwargs)

        env_dict = (new_args[0] or {})
        if not ASSET_PATH.match(env_dict['PATH_INFO']) and \
           not HEALTH_CHECK_PATH.match(env_dict['PATH_INFO']):
            if db.is_closed():
                db.connect()

        # finished callbacks
        self.add_finished_callback(self.__class__.close_db)
        self.add_finished_callback(self._set_hsts)

    @classmethod
    def trim_port(cls, env_dict):
        """Removes port from links.
        """
        http_host = env_dict.get('HTTP_HOST', '')
        http_host = re.sub(':[0-9]+$', '', http_host)

        env_dict['HTTP_HOST'] = http_host
        env_dict['SERVER_PORT'] = ''
        return env_dict

    @classmethod
    def close_db(cls, _req):
        """Closes database connection if it's not closed.
        """
        if not db.is_closed():
            db.close()

    @property
    def settings(self):
        """Gets settings dict.
        """
        from aarau import get_settings

        return get_settings() or {}

    # see https://github.com/Pylons/webob/issues/77
    @reify
    def remote_ip(self):
        """Calculates client's ip address.
        """
        from collections import OrderedDict
        import itertools

        raw_remote_addr = self._ips_at('REMOTE_ADDR')

        remote_addr = raw_remote_addr[-1] if raw_remote_addr else None
        client_ips = self._ips_at('HTTP_CLIENT_IP')[::-1]
        forwarded_ips = self._ips_at('HTTP_X_FORWARDED_FOR')[::-1]

        # ip snoofing check
        if (client_ips and client_ips[-1]) and \
           (forwarded_ips and forwarded_ips[-1]) and \
           (client_ips[-1] not in forwarded_ips):
            # pylint: disable=no-member
            raise Exception(
                'It may be IP snoofing attack! '
                'HTTP_CLIENT_IP: {0!s} HTTP_X_FORWARDED_FOR: {1!s}'.format(
                    self.environ.get('HTTP_CLIENT_IP'),
                    self.environ.get('HTTP_X_FORWARDED_FOR')))

        ips = list(OrderedDict.fromkeys(itertools.chain.from_iterable(
            [forwarded_ips, client_ips, [remote_addr]])))

        found_trusted_ips = False
        for ip in ips:
            ip_addr = ipaddress.ip_address(ip)
            for tp in TRUSTED_NETWORKS:
                if ip_addr in tp:
                    found_trusted_ips = True
                    break

        return ips[0] if found_trusted_ips else remote_addr

    def _ips_at(self, header):
        """Returns valid ip address only.
        """
        value = self.environ.get(header, None)  # pylint: disable=no-member
        ips = re.split(r'[,\s]+', value) if value else []
        return [ip for ip in ips if IPV4_ADDR.match(ip) or IPV6_ADDR.match(ip)]

    def _set_hsts(self, req):
        """Sets HSTS Header based on `X-Forwarded-Proto`.
        """
        criteria = [
            (not self.env.is_production),
            req.headers.get('X-Forwarded-Proto', 'http') == 'https',
        ]
        if not any(criteria):
            hsts_max_age = self.settings.get('hsts.max-age', '3153600')
            hsts_options = self.settings.get('hsts.options', '')
            req.response.headers['Strict-Transport-Security'] = \
                "max-age={};{}".format(hsts_max_age, hsts_options)

    def _force_ssl(self, env_dict):
        """Set url schema forcing https for next request links.
        """
        env_dict['wsgi.url_scheme'] = self.settings.get(
            'wsgi.url_scheme', 'https')
        return env_dict
