"""View actions for login/logout.
"""

from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember, forget
from pyramid.view import view_config

from aarau.models.user import User
from aarau.views import tpl


@view_config(route_name='login', request_method=('GET', 'POST'),
             renderer=tpl('shared/login.mako'))
def login(req):
    """Renders login view and authenticate user via POST.
    """
    next_path = req.params.get('next', req.referrer)
    if not next_path or 'login' in next_path:
        next_path = req.route_path('top')
    user = req.user
    if user is not None:
        headers = remember(req, user.id)
        return HTTPFound(location=next_path, headers=headers)
    email = ''
    if 'submit' in req.POST:
        email = req.params['email']
        password = req.params['password']
        user = User.select().where(
            User.activation_state == 'active', User.email == email).first()
        if user is not None and user.verify_password(password):
            headers = remember(req, user.id)
            return HTTPFound(location=next_path, headers=headers)
        _ = req.translate
        req.session.flash(_('login.failure'),
                          queue='failure',
                          allow_duplicate=False)

    return dict(next_path=next_path, email=email)


@view_config(route_name='logout')
def logout(req):
    """Sets user as logged out and redirects to top view.
    """
    headers = forget(req)
    return HTTPFound(
        location=req.route_url('top', namespace=None), headers=headers)
