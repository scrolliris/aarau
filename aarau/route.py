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


def define_registry_routes(c, namespace):
    c.add_route('registry.search', '/')

    c.add_route('registry.site.overview',
                '/{namespace}/{slug}',
                custom_predicates=(namespace,))


def define_console_routes(c, namespace):
    c.add_route('console.top', '/')

    # project
    c.add_route('console.project.new', '/projects/new')
    c.add_route('console.project.settings', '/projects/{namespace}/settings',
                custom_predicates=(namespace,))
    c.add_route('console.project.overview', '/projects/{namespace}',
                custom_predicates=(namespace,))

    # settings
    c.add_route('console.settings', '/settings')
    c.add_route('console.settings.section', '/settings/{section}')
    c.add_route('console.settings.email_delete',
                '/settings/email/delete')
    c.add_route('console.settings.email_change',
                '/settings/email/change')
    c.add_route('console.settings.email_activate',
                '/settings/email/confirm/{token}')

    # site
    c.add_route('console.site.new',
                '/projects/{namespace}/sites/new',
                custom_predicates=(namespace,))
    # site:application - insights
    c.add_route('console.site.insights',
                '/projects/{namespace}/sites/{slug}/insights',
                custom_predicates=(namespace,))
    # site:application - settings
    c.add_route('console.site.settings.scripts',
                '/projects/{namespace}/sites/{slug}/settings/scripts',
                custom_predicates=(namespace,))
    c.add_route('console.site.settings.widgets',
                '/projects/{namespace}/sites/{slug}/settings/widgets',
                custom_predicates=(namespace,))
    c.add_route('console.site.settings.badges',
                '/projects/{namespace}/sites/{slug}/settings/badges',
                custom_predicates=(namespace,))
    c.add_route('console.site.settings',
                '/projects/{namespace}/sites/{slug}/settings',
                custom_predicates=(namespace,))
    # site - overview
    c.add_route('console.site.overview',
                '/projects/{namespace}/sites/{slug}',
                custom_predicates=(namespace,))

    # article
    c.add_route('console.article.list',
                '/projects/{namespace}/sites/{slug}/articles',
                custom_predicates=(namespace,))
    c.add_route('console.article.editor.new',
                '/projects/{namespace}/sites/{slug}/editor',
                custom_predicates=(namespace,))
    c.add_route('console.article.editor.edit',
                '/projects/{namespace}/sites/{slug}/editor',
                custom_predicates=(namespace,))

    # -- internal api
    url_base = '/api/projects/{namespace}/sites/{slug}'

    # classification
    c.add_route('console.api.classification.tree',
                '{0:s}/classifications/tree.json'.format(url_base),
                custom_predicates=(namespace,))
    # article
    c.add_route('console.api.article.editor',
                '{0:s}/articles/editor.json'.format(url_base),
                custom_predicates=(namespace,))
    c.add_route('console.api.article.settings',
                '{0:s}/articles/settings.json'.format(url_base),
                custom_predicates=(namespace,))
    c.add_route('console.api.article.progress_states',
                '{0:s}/articles/{1:s}/progress_states.json'.format(
                    url_base, '{code}'),
                custom_predicates=(namespace,))
    # insights
    c.add_route('console.api.site.insights.data',
                '{0:s}/insights/data.json'.format(url_base),
                custom_predicates=(namespace,))
    c.add_route('console.api.site.insights.metrics',
                '{0:s}/insights/metrics.json'.format(url_base),
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
