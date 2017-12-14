import os
import json
import re
from typing import Union
from urllib import parse

from bleach import clean as _clean
from markupsafe import Markup

from pyramid.decorator import reify
from pyramid.events import subscriber
from pyramid.events import BeforeRender

from aarau.env import Env
from aarau.request import CustomRequest

UNSLASH_PATTERN = re.compile(r'^\/|\/$')


@subscriber(BeforeRender)
def add_template_util_renderer_globals(evt) -> None:
    """Adds template utility instance as `util`."""
    ctx, req = evt['context'], evt['request']
    util = getattr(req, 'util', None)

    if util is None and req is not None:
        from .. import get_settings

        util = get_settings()['aarau.includes']['template_util'](ctx, req)
    evt['util'] = util
    evt['clean'] = clean
    evt['unquote'] = unquote
    evt['formatting'] = formatting


def clean(**kwargs) -> 'function':
    """Returns sanitized value except allowed tags and attributes.

    It looks like `${'<a href="/"><em>link</em></a>'|n,clean(
    tags=['a'], attributes=['href'])}`.

    >>> from aarau.utils.template import clean

    >>> type(clean(tags=['a'], attributes=['href']))
    <class 'function'>

    >>> c = clean(tags=['a'], attributes=['href'])
    >>> str(c('<a href="/"><em>link</em></a>'))
    '<a href="/">&lt;em&gt;link&lt;/em&gt;</a>'
    """
    def __clean(text) -> Markup:
        return Markup(_clean(text, **kwargs))

    return __clean


def unquote(text: str) -> str:
    """Returns unquoted text (decorded url)."""
    return parse.unquote(text)


def formatting(*args: tuple) -> 'function':
    """Returns formatted value if text has placeholder."""
    def __formatting(text: str) -> str:
        return str(text).format(*args)

    return __formatting


class TemplateUtil(object):
    # pylint: disable=no-self-use
    """The utility for templates.

    In some cases, no-self-use is disabled for convenience at templates.
    """

    def __init__(self, ctx: dict, req: CustomRequest, **kwargs: dict) -> None:
        self.ctx, self.req = ctx, req

        self.env = Env()

        if getattr(req, 'util', None) is None:
            req.util = self
        self.__dict__.update(kwargs)

    @reify
    def route_name(self) -> Union[None, str]:
        """Returns matched route name."""
        route = self.req.matched_route
        if route:
            return route.name

    @reify
    def manifest_json(self) -> dict:
        """Reads manifest.json as dict."""
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

    def is_matched(self, matchdict) -> bool:
        """Returns bool if dict matches or not."""
        return self.req.matchdict == matchdict

    def static_url(self, filepath) -> str:
        """Returns url for asset file path.

        If producition, generates bucket url which is hosted on CDN.
        """
        def get_bucket_info(name):
            part = self.req.settings.get('bucket.{0:s}'.format(name))
            return re.sub(UNSLASH_PATTERN, '', part)

        if self.env.is_production:
            h, n, p = [get_bucket_info(x) for x in ('host', 'name', 'path')]
            return 'https://{0:s}/{1:s}/{2:s}/{3:s}'.format(h, n, p, filepath)
        return self.req.static_url('aarau:../static/' + filepath)

    def static_path(self, filepath) -> str:
        return self.req.static_path('aarau:../static/' + filepath)

    def hashed_asset_url(self, filepath) -> str:
        """Returns url path for static file with content hash.

        Hash value is extract from manifest.json which is generated via gulp
        cammand.
        """
        hashed_filepath = self.manifest_json.get(filepath, filepath)
        return self.static_url(hashed_filepath)

    def truncate(self, str_val, length=25, suffix='...') -> str:
        """Returns new truncated string and appends suffix."""
        if not isinstance(str_val, str):
            return ''
        if len(str_val) > length:
            str_val = str_val[:length - len(suffix)] + suffix
        return str_val
