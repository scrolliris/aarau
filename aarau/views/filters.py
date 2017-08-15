from functools import wraps

from pyramid.httpexceptions import HTTPFound, HTTPForbidden
from pyramid.view import forbidden_view_config


def login_required(f):
    @wraps(f)
    def authentication_user(*args, **kwargs):
        # TODO: check this is valid way
        request = args[-1]
        user = request.user
        if not user:
            raise HTTPForbidden
        # TODO check permission
        # TODO check joined_projects (reduce a query)
        if request.subdomain == 'console' and not user.projects:
            raise HTTPForbidden
        return f(request, **kwargs)
    return authentication_user


@forbidden_view_config()
def forbidden_redirect(request):
    _ = request.translate
    if request.authenticated_userid:
        # return Response('forbidden')
        return HTTPFound(location=request.route_url('top', namespace=None))
    else:
        request.session.flash(_('login.needed'),
                              queue='error', allow_duplicate=False)
        return HTTPFound(location=request.route_url('login', namespace=None))
