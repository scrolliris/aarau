from datetime import datetime
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound, HTTPNotFound

from ...models.user import User
from ...tasks.send_email import send_reset_password_email
from .forms import (
    reset_password_request_form_factory,
    reset_password_form_factory,
)


@view_config(route_name='reset_password.request',
             request_method=('GET', 'POST'),
             renderer='../../templates/shared/reset_password_request.mako')
def reset_password_request(request):
    user = request.user
    if user:
        return HTTPFound(location=request.route_path('top'))

    form = reset_password_request_form_factory(request)
    if 'submit' in request.POST:
        _ = request.translate
        if form.validate():
            email = form.email.data
            user = User.select().where(
                User.activation_state == 'active', User.email == email).first()
            if user and user.generate_reset_password_token():
                user.save()
                send_reset_password_email.delay(user.id)

            request.session.flash(_('reset_password.request.success'),
                                  queue='success',
                                  allow_duplicate=False)
            return HTTPFound(location=request.route_path(
                'reset_password.request'))
        else:
            request.session.flash(_('reset_password.request.failure'),
                                  queue='error',
                                  allow_duplicate=False)
    return dict(form=form)


# TODO: move reset password service
@view_config(route_name='reset_password',
             request_method=('GET', 'POST'),
             renderer='../../templates/shared/reset_password.mako')
def reset_password(request):
    user = request.user
    if user:
        return HTTPFound(location=request.route_path('top'))

    token = request.matchdict['token']
    try:
        user = User.select().where(
            User.activation_state == 'active',
            User.reset_password_token == token).get()
    except:
        raise HTTPNotFound

    _ = request.translate
    if user.reset_password_token_expires_at < datetime.utcnow():
        request.session.flash(_('reset_password.update.expired'),
                              queue='error', allow_duplicate=False)
        return HTTPFound(location=request.route_path('reset_password'))

    form = reset_password_form_factory(request)
    if 'submit' in request.POST:
        if form.validate():
            user.reset_password(token, form.new_password.data)
            request.session.flash(_('reset_password.update.success'),
                                  queue='success', allow_duplicate=False)
            return HTTPFound(location=request.route_path('login'))
        else:
            request.session.flash(_('reset_password.update.failure'),
                                  queue='error', allow_duplicate=False)
    return dict(token=token, form=form)
