from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember, forget
from pyramid.view import view_config

from aarau.models.user import User
from aarau.views import tpl


def get_next_path(req, except_paths=()):
    """Returns next_path which is extracted params or referrer if possible."""
    path = req.params.get('next_path', req.referrer) or ''

    scheme = req.settings.get('wsgi.url_scheme', 'https')
    domain = req.settings.get('domain', 'localhost')
    # fmt: off
    if not path.startswith('{0:s}://{1:s}'.format(scheme, domain)) and \
       not path.startswith('{0:s}://console.{1:s}'.format(scheme, domain)):
        path = req.route_path('top')
    # fmt: on

    if [p for p in except_paths if p in path]:
        path = req.route_path('top')

    return path


@view_config(
    route_name='login',
    request_method=('GET', 'POST'),
    renderer=tpl('shared/login.mako'),
)
def login(req):
    """Renders login view and authenticate user via POST."""
    next_path = get_next_path(req, except_paths=('/login', '/logout'))
    user = req.user
    if user is not None:
        headers = remember(req, user.id)
        return HTTPFound(location=next_path, headers=headers)
    email = ''
    if 'submit' in req.POST:
        email = req.params['email']
        password = req.params['password']
        # fmt: off
        user = User.select().where(
            User.activation_state == 'active', User.email == email).first()
        # fmt: on
        if user is not None and user.verify_password(password):
            headers = remember(req, user.id)
            return HTTPFound(location=next_path, headers=headers)
        _ = req.translate
        req.session.flash(
            _('login.failure'), queue='failure', allow_duplicate=False
        )

    return dict(next_path=next_path, email=email)


@view_config(route_name='logout')
def logout(req):
    """Sets user as logged out and redirects to top view."""
    headers = forget(req)
    return HTTPFound(
        location=req.route_url('top', namespace=None), headers=headers
    )
