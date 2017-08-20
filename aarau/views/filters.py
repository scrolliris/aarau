from functools import wraps

from pyramid.httpexceptions import HTTPFound, HTTPForbidden
from pyramid.view import forbidden_view_config


def login_required(f):
    @wraps(f)
    def authentication_user(*args, **kwargs):
        # TODO: check this is valid way
        req = args[-1]
        user = req.user
        if not user:
            raise HTTPForbidden
        # TODO check permission
        # TODO check joined_projects (reduce a query)
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
    else:
        req.session.flash(_('login.needed'),
                          queue='error', allow_duplicate=False)
        return HTTPFound(location=req.route_url('login', namespace=None))
