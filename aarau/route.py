from contextlib import contextmanager
from os import path
import time

from pyramid.static import QueryStringConstantCacheBuster

from aarau.env import Env


class SubdomainPredicate(object):
    def __init__(self, val, _config):
        self.val = val

    def text(self):
        return 'subdomain = %s' % str(self.val)

    phash = text

    def __call__(self, context, request):
        subdomain = request.subdomain
        if subdomain is None:
            subdomain = ''
        return str(subdomain) == self.val


def subdomain_pregenerator(subdomain):
    env = Env()

    def pregenerator(_req, elements, kw):
        domain = env.get('DOMAIN', None)
        if subdomain:
            kw['_host'] = '{0!s}.{1!s}'.format(subdomain, domain)
        else:
            kw['_host'] = '{0!s}'.format(domain)
        return elements, kw
    return pregenerator


def subdomain_manager(config):
    @contextmanager
    def subdomain(subdomain=None):
        if subdomain is None:
            subdomain = ''
        pregenerator = subdomain_pregenerator(subdomain)

        original_add_route = config.__class__.add_route

        def add_route(self, *args, **kw):
            kw['subdomain'] = subdomain
            kw['pregenerator'] = pregenerator
            original_add_route(self, *args, **kw)

        try:
            import types
            config.add_route = types.MethodType(add_route, config)
            yield config
        finally:
            config.add_route = types.MethodType(original_add_route, config)

    return subdomain


def subdomain_manager_factory(config):
    config.add_route_predicate('subdomain', SubdomainPredicate)
    return subdomain_manager(config)


def site_type_of(hosting_type):
    def predicate(_, req):
        if 'type' not in req.params or req.params['type'] != hosting_type:
            return False
        return True
    return predicate


def includeme(config):
    env = Env()

    # see also __init__.py for static files
    cache_max_age = 3600 if env.is_production else 0

    static_dir = path.join(path.dirname(path.abspath(__file__)), '../static')
    filenames = [f for f in ('robots.txt', 'humans.txt', 'favicon.ico')
                 if path.isfile((static_dir + '/{}').format(f))]
    if filenames:
        filenames = sum([filenames, []], [])
        config.add_asset_views(
            'aarau:../static', filenames=filenames, http_cache=cache_max_age)

    config.add_static_view(
        name='assets', path='aarau:../static/', cache_max_age=cache_max_age)
    config.add_cache_buster('aarau:../static/', QueryStringConstantCacheBuster(
        str(int(time.time()))))

    subdomain = subdomain_manager_factory(config)

    with subdomain('console') as c:
        # pylint: disable=anomalous-backslash-in-string
        c.add_route('console.top', '/')
        c.add_route('console.project.new', '/project/new')
        c.add_route('console.project.view', '/project/{id:\d+}')
        c.add_route('console.project.edit', '/project/{id:\d+}/edit')

        # application
        application_type = site_type_of('application')
        c.add_route('console.site.application.new',
                    '/project/{project_id:\d+}/site/new',
                    custom_predicates=(application_type,))
        c.add_route('console.site.application.edit',
                    '/project/{project_id:\d+}/site/{id:\d+}/edit',
                    custom_predicates=(application_type,))
        c.add_route('console.site.application.view.result',
                    '/project/{project_id:\d+}/site/{id:\d+}/result',
                    custom_predicates=(application_type,))
        c.add_route('console.site.application.view.script',
                    '/project/{project_id:\d+}/site/{id:\d+}/script',
                    custom_predicates=(application_type,))
        c.add_route('console.site.application.view.badge',
                    '/project/{project_id:\d+}/site/{id:\d+}/badge',
                    custom_predicates=(application_type,))

        # publication
        publication_type = site_type_of('publication')
        c.add_route('console.site.publication.new',
                    '/project/{project_id:\d+}/site/new',
                    custom_predicates=(publication_type,))
        c.add_route('console.site.publication.edit',
                    '/project/{project_id:\d+}/site/{id:\d+}/edit',
                    custom_predicates=(publication_type,))
        c.add_route('console.site.publication.view',
                    '/project/{project_id:\d+}/site/{id:\d+}',
                    custom_predicates=(publication_type,))

    # internal api
    with subdomain('console') as c:
        # pylint: disable=anomalous-backslash-in-string
        c.add_route('api.console.site.application.result',
                    '/api/project/{project_id:\d+}/site/{id:\d+}/result.json',
                    custom_predicates=(application_type,))

    with subdomain(None) as c:
        c.add_route('top', '/')

        c.add_route('login', '/login')
        c.add_route('logout', '/logout')

        c.add_route('reset_password.request', '/password/reset')
        c.add_route('reset_password', '/password/reset/{token}')

        c.add_route('signup', '/signup')
        c.add_route('signup.activate', '/user/activate/{token}')

        # login_required
        c.add_route('project.new', '/project/new')

        c.add_route('settings', '/settings')
        c.add_route('settings.section', '/settings/{section}')

        c.add_route('settings.email_delete',
                    '/settings/email/delete')
        c.add_route('settings.email_change',
                    '/settings/email/change')
        c.add_route('settings.email_activate',
                    '/settings/email/confirm/{token}')
