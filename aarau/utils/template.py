"""Template utility class and helper functions.
"""
from os import path
import json

from bleach import clean as _clean
from markupsafe import Markup

from pyramid.decorator import reify
from pyramid.events import subscriber
from pyramid.events import BeforeRender


@subscriber(BeforeRender)
def add_template_util_renderer_globals(evt):
    """Adds template utility instance as `util`.
    """
    ctx, req = evt['context'], evt['request']
    util = getattr(req, 'util', None)

    if util is None and req is not None:
        from .. import get_settings

        util = get_settings()['aarau.includes']['template_util'](ctx, req)
    evt['util'] = util
    evt['clean'] = clean


def clean(**kwargs) -> 'function':
    """Returns sanitized value except allowed tags and attributes.

    >>> ${'<a href="/"><em>link</em></a>'|n,clean(
            tags=['a'], attributes=['href'])}
    "<a href=\"/\">link</a>"
    """
    def __clean(text) -> Markup:
        return Markup(_clean(text, **kwargs))

    return __clean



class TemplateUtil(object):
    """The utility for templates.
    """
    def __init__(self, ctx, req, **kwargs):
        self.ctx, self.req = ctx, req

        if getattr(req, 'util', None) is None:
            req.util = self
        self.__dict__.update(kwargs)

    @reify
    def route_name(self):
        route = self.req.matched_route
        if route:
            return route.name

    @reify
    def manifest_json(self):
        manifest_file = path.join(
            path.dirname(__file__), '..', '..', 'static', 'manifest.json')
        data = {}
        if path.isfile(manifest_file):
            with open(manifest_file) as data_file:
                data = json.load(data_file)
        return data

    @reify
    def typekit_id(self):
        from ..env import Env
        env = Env()
        return env.get('TYPEKIT_ID', '')

    def is_matched(self, matchdict):
        return self.req.matchdict == matchdict

    def static_url(self, path):
        return self.req.static_url('aarau:../static/' + path)

    def static_path(self, path):
        return self.req.static_path('aarau:../static/' + path)

    def built_asset_url(self, path):
        path = self.manifest_json.get(path, path)
        return self.static_url(path)

    def truncate(self, str_val, limit):
        if not isinstance(str_val, str):
            return ''
        if len(str_val) > limit:
            str_val = str_val[:limit-3] + '...'
        return str_val
