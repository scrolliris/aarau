from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.security import remember
from pyramid.view import view_config

from aarau.models.user import User
from aarau.services.interface import IActivator
from aarau.views import tpl
from aarau.views.signup.form import build_signup_form


@view_config(route_name='signup', request_method=('GET', 'POST'),
             renderer=tpl('shared/signup.mako'))
def signup(request):
    """Renders signup view and creates new user account via POST."""
    user = request.user
    if user:
        return HTTPFound(location=request.route_path('top'))

    _ = request.translate
    form = build_signup_form(request)
    if 'submit' in request.POST:
        if form.validate():
            user = User(email=form.email.data, name=form.name.data,
                        username=form.username.data)
            user.set_password(form.password.data)

            activator = request.find_service(iface=IActivator, name='account')
            activator.assign(user=user)
            activator.invoke()

            request.session.flash(_('signup.creation.success'),
                                  queue='success', allow_duplicate=False)
            return HTTPFound(location=request.route_path('signup'))
        else:
            request.session.flash(_('signup.creation.failure'),
                                  queue='failure', allow_duplicate=False)

    return dict(form=form)


@view_config(route_name='signup.activate', request_method='GET')
def signup_activate(request):
    """Activates user account using token."""
    user = request.user
    if user:
        return HTTPFound(location=request.route_path('top'))

    try:
        activator = request.find_service(iface=IActivator, name='account')
        activator.assign(token=request.matchdict.get('token'))
    except Exception:
        raise HTTPNotFound
    else:
        _ = request.translate

        if activator.has_token_expired():
            request.session.flash(_('signup.activation.expired'),
                                  queue='failure', allow_duplicate=False)
        elif not activator.activate():
            request.session.flash(_('signup.activation.failure'),
                                  queue='failure', allow_duplicate=False)
        else:
            request.session.flash(_('signup.activation.success'),
                                  queue='success', allow_duplicate=False)
            next_path = request.route_path('console.top')
            headers = remember(request, activator.user.id)
            return HTTPFound(location=next_path, headers=headers)
    next_path = request.route_path('signup')
    return HTTPFound(location=next_path)
