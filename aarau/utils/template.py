"""Template utility class and helper functions
"""
import os
import json
from typing import Union

from bleach import clean as _clean
from markupsafe import Markup

from pyramid.decorator import reify
from pyramid.events import subscriber
from pyramid.events import BeforeRender

from aarau.request import CustomRequest


@subscriber(BeforeRender)
def add_template_util_renderer_globals(evt) -> None:
    """Adds template utility instance as `util`
    """
    ctx, req = evt['context'], evt['request']
    util = getattr(req, 'util', None)

    if util is None and req is not None:
        from .. import get_settings

        util = get_settings()['aarau.includes']['template_util'](ctx, req)
    evt['util'] = util
    evt['clean'] = clean


def clean(**kwargs) -> 'function':
    """Returns sanitized value except allowed tags and attributes

    >>> ${'<a href="/"><em>link</em></a>'|n,clean(
            tags=['a'], attributes=['href'])}
    "<a href="/">link</a>"
    """
    def __clean(text) -> Markup:
        return Markup(_clean(text, **kwargs))

    return __clean


class TemplateUtil(object):
    """The utility for templates

    In some cases, no-self-use is disabled for convenience at templates
    """
    def __init__(self, ctx: dict, req: CustomRequest, **kwargs: dict) -> None:
        self.ctx, self.req = ctx, req

        if getattr(req, 'util', None) is None:
            req.util = self
        self.__dict__.update(kwargs)

    @reify
    def route_name(self) -> Union[None, str]:
        """Returns matched route name
        """
        route = self.req.matched_route
        if route:
            return route.name

    @reify
    def manifest_json(self) -> dict:  # pylint: disable=no-self-use
        """Reads manifest.json as dict
        """
        manifest_file = os.path.join(
            os.path.dirname(__file__), '..', '..', 'static', 'manifest.json')
        data = {}
        if os.path.isfile(manifest_file):
            try:
                with open(manifest_file) as data_file:
                    data = json.load(data_file)
            except (IOError, ValueError):
                pass

        return data

    @reify
    def typekit_id(self) -> str:  # pylint: disable=no-self-use
        """Return typekit id from env
        """
        from ..env import Env
        env = Env()
        return str(env.get('TYPEKIT_ID', ''))

    def is_matched(self, matchdict) -> bool:
        """Returns bool if dict matches or not
        """
        return self.req.matchdict == matchdict

    def static_url(self, path) -> str:
        """Returns whole url for static file
        """
        return self.req.static_url('aarau:../static/' + path)

    def static_path(self, path) -> str:
        """Returns url path for static file
        """
        return self.req.static_path('aarau:../static/' + path)

    def built_asset_url(self, path) -> str:
        """Returns url path for static file with built hash from manifest.json
        """
        path = self.manifest_json.get(path, path)
        return self.static_url(path)

    def truncate(self, str_val, length=25, suffix='...') -> str:  # pylint: disable=no-self-use
        """Returns new truncated string and appends suffix
        """
        if not isinstance(str_val, str):
            return ''
        if len(str_val) > length:
            str_val = str_val[:length - len(suffix)] + suffix
        return str_val
