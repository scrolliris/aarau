from functools import wraps

from pyramid.httpexceptions import HTTPFound, HTTPForbidden
from pyramid.view import forbidden_view_config


def login_required(f):
    @wraps(f)
    def authentication_user(*args, **kwargs):
        # TODO: Check this is valid way
        req = args[-1]
        user = req.user
        if not user:
            raise HTTPForbidden
        # TODO: Check permission
        # TODO: Check joined_projects (reduce a query)
        if req.subdomain == 'console' and not user.projects:
            raise HTTPForbidden
        return f(req, **kwargs)
    return authentication_user


@forbidden_view_config()
def forbidden_redirect(req):
    _ = req.translate
    if req.authenticated_userid:
        # return Response('forbidden')
        return HTTPFound(location=req.route_url('top', namespace=None))

    req.session.flash(_('login.needed'),
                      queue='failure', allow_duplicate=False)
    return HTTPFound(location=req.route_url('login', namespace=None))


def namespace_filter():
    import re
    # reuse from a pattern for validator in form
    from aarau.views.console.project.form import NAMESPACE_PATTERN

    pattern = re.compile(NAMESPACE_PATTERN)

    def filter_(namespace):
        if not namespace:
            return False
        return pattern.match(namespace)
    return filter_
