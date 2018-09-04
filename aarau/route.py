from contextlib import contextmanager
from os import path
import time

from pyramid.static import QueryStringConstantCacheBuster

from aarau.env import Env


class SubdomainPredicate():
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


def namespace_predicator():
    from aarau.views.filter import namespace_filter

    filter_ = namespace_filter()

    def predicate(inf, _):
        match = inf.get('match', {})
        if not match:
            return False
        return filter_(match.get('namespace', None))
    return predicate


def define_carrell_routes(c):
    c.add_route('carrell.top', '/')

    # settings
    c.add_route('carrell.settings', '/settings')
    c.add_route('carrell.settings.section', '/settings/{section}')
    c.add_route('carrell.settings.email_delete',
                '/settings/email/delete')
    c.add_route('carrell.settings.email_change',
                '/settings/email/change')
    c.add_route('carrell.settings.email_activate',
                '/settings/email/confirm/{token}')


def define_registry_routes(c, namespace):
    c.add_route('registry.search', '/')

    c.add_route('registry.site.overview',
                '/{namespace}/{slug}',
                custom_predicates=(namespace,))


def define_console_routes(c, namespace):
    c.add_route('console.top', '/')

    # project
    c.add_route('console.project.new', '/projects/new')
    c.add_route('console.project.edit', '/{namespace}/edit',
                custom_predicates=(namespace,))
    c.add_route('console.project.overview', '/{namespace}',
                custom_predicates=(namespace,))

    # site
    c.add_route('console.site.new',
                '/{namespace}/new',
                custom_predicates=(namespace,))
    # site:application - insights
    c.add_route('console.site.insights',
                '/{namespace}/{slug}/insights',
                custom_predicates=(namespace,))
    # site:application - settings
    c.add_route('console.site.settings.scripts',
                '/{namespace}/{slug}/settings/scripts',
                custom_predicates=(namespace,))
    c.add_route('console.site.settings.widgets',
                '/{namespace}/{slug}/settings/widgets',
                custom_predicates=(namespace,))
    c.add_route('console.site.settings.badges',
                '/{namespace}/{slug}/settings/badges',
                custom_predicates=(namespace,))
    c.add_route('console.site.settings',
                '/{namespace}/{slug}/settings',
                custom_predicates=(namespace,))
    # site - overview
    c.add_route('console.site.overview',
                '/{namespace}/{slug}',
                custom_predicates=(namespace,))

    # article
    c.add_route('console.article.list',
                '/{namespace}/{slug}/articles',
                custom_predicates=(namespace,))
    c.add_route('console.article.editor.new',
                '/{namespace}/{slug}/editor',
                custom_predicates=(namespace,))
    c.add_route('console.article.editor.edit',
                '/{namespace}/{slug}/editor',
                custom_predicates=(namespace,))

    # internal api - article
    c.add_route('api.console.article.editor',
                '/api/{namespace}/{slug}/article/editor.json',
                custom_predicates=(namespace,))
    c.add_route('api.console.article.config',
                '/api/{namespace}/{slug}/article/config.json',
                custom_predicates=(namespace,))
    # internal api - insights
    c.add_route('api.console.site.insights',
                '/api/projects/{namespace}/{slug}/insights.json',
                custom_predicates=(namespace,))


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

    namespace = namespace_predicator()
    with subdomain('console') as c:
        define_console_routes(c, namespace)

    with subdomain('carrell') as c:
        define_carrell_routes(c)

    with subdomain('registry') as c:
        define_registry_routes(c, namespace)

    with subdomain(None) as c:
        c.add_route('top', '/')

        c.add_route('login', '/login')
        c.add_route('logout', '/logout')

        c.add_route('signup', '/signup')

        c.add_route('signup.activate', '/activate/{token}')
        c.add_route('reset_password.request', '/password/reset')
        c.add_route('reset_password', '/password/reset/{token}')

        # login required
        c.add_route('project.new', '/projects/new')

    # public view
    with subdomain(None) as c:
        c.add_route('publication', '/{namespace}/{slug}')
        c.add_route('article', '/{namespace}/{slug}/{path}')
