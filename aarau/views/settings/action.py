"""View actions for settings.
"""

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound, HTTPNotFound

from aarau.models.user_email import UserEmail
from aarau.services.interface import IActivator
from aarau.views import tpl
from aarau.views.filters import login_required
from aarau.views.settings.form import (
    change_password_form_factory,
    new_email_form_factory,
    delete_email_form_factory,
    change_email_form_factory,
)


@view_config(route_name='settings',
             renderer=tpl('settings/account.mako'))
@view_config(route_name='settings.section', match_param='section=account',
             renderer=tpl('settings/account.mako'))
@login_required
def settings_account(_request):
    """ Renders account settings view
    """
    return {}


@view_config(route_name='settings.section', match_param='section=email',
             request_method=('GET', 'POST'),
             renderer=tpl('settings/email.mako'))
@login_required
def settings_email(request):
    """ Renders email settings view and adds new email via POST
    """
    user = request.user

    next_path = request.route_path('settings.section', section='email')
    user_emails = user.emails.order_by(
        UserEmail.type.asc(), UserEmail.id.asc())

    form = new_email_form_factory(request)
    if 'submit' in request.POST:
        _ = request.translate
        if 'pending' in [ue.activation_state for ue in user_emails]:
            request.session.flash(_('settings.email.addition.pending'),
                                  queue='warning', allow_duplicate=False)
            return HTTPFound(location=next_path)
        if form.validate():
            activator = request.find_service(
                iface=IActivator, name='user_email')
            activator.assign(email=form.new_email.data, user=user)
            activator.invoke()
            request.session.flash(_('settings.email.addition.success'),
                                  queue='success', allow_duplicate=False)
            return HTTPFound(location=next_path)
        else:
            request.session.flash(_('settings.email.addition.failure'),
                                  queue='error', allow_duplicate=False)

    email_forms = {}
    for user_email in user_emails:
        email_forms[user_email.id] = {
            'change': change_email_form_factory(request, user_email),
            'delete': delete_email_form_factory(request, user_email),
        }
    return dict(form=form, user_emails=user_emails, email_forms=email_forms)


@view_config(route_name='settings.email_activate', request_method='GET')
@login_required
def settings_email_activate(request):
    """ Activates user email
    """
    user = request.user

    try:
        activator = request.find_service(IActivator, name='user_email')
        activator.assign(token=request.matchdict['token'], user=user)
    except:
        raise HTTPNotFound
    else:
        _ = request.translate

        if activator.has_token_expired():
            request.session.flash(_('settings.email.confirmation.expired'),
                                  queue='error', allow_duplicate=False)
        elif not activator.activate():
            request.session.flash(_('settings.email.confirmation.failure'),
                                  queue='error', allow_duplicate=False)
        else:
            request.session.flash(_('settings.email.confirmation.success'),
                                  queue='success', allow_duplicate=False)
    return HTTPFound(location=request.route_path(
        'settings.section', section='email'))


@view_config(route_name='settings.email_delete', request_method='POST')
@login_required
def settings_email_delete(request):
    """ Deletes user email
    """
    user = request.user
    user_email = user.emails.where(
        UserEmail.email == request.params['email'],
        UserEmail.type != 'primary',
    ).first()

    form = delete_email_form_factory(request, user_email)
    if 'submit' in request.POST:
        _ = request.translate
        if form.validate():
            user_email.delete_instance()
            request.session.flash(_('settings.email.deletion.success'),
                                  queue='success', allow_duplicate=False)
        else:
            request.session.flash(_('settings.email.deletion.failure'),
                                  queue='error', allow_duplicate=False)

    return HTTPFound(location=request.route_path(
        'settings.section', section='email'))


@view_config(route_name='settings.email_change', request_method='POST')
@login_required
def settings_email_change(request):
    """ Changes user email
    """
    user = request.user
    user_email = user.emails.where(
        UserEmail.email == request.params['email'],
        UserEmail.type != 'primary',
    ).first()

    form = change_email_form_factory(request, user_email)
    if 'submit' in request.POST:
        _ = request.translate
        if form.validate() and user_email.make_as_primary():
            request.session.flash(_('settings.email.change.success'),
                                  queue='success', allow_duplicate=False)
        else:
            request.session.flash(_('settings.email.change.failure'),
                                  queue='error', allow_duplicate=False)

    return HTTPFound(location=request.route_path(
        'settings.section', section='email'))


@view_config(route_name='settings.section', match_param='section=password',
             request_method=('GET', 'POST'),
             renderer=tpl('settings/password.mako'))
@login_required
def settings_password(request):
    """ Renders password settings view and changes password via POST
    """
    user = request.user

    form = change_password_form_factory(request, user)
    if 'submit' in request.POST:
        _ = request.translate
        if form.validate():
            if user.verify_password(form.current_password.data):
                user.set_password(form.new_password.data)
                user.save()
                request.session.flash(_('settings.password.change.success'),
                                      queue='success', allow_duplicate=False)
                return HTTPFound(location=request.route_path(
                    'settings.section', section='password'))
            else:
                request.session.flash(_('settings.password.change.invalid'),
                                      queue='error', allow_duplicate=False)
        else:
            request.session.flash(_('settings.password.change.failure'),
                                  queue='error', allow_duplicate=False)
    return dict(form=form)
