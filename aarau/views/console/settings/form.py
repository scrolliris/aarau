from wtforms import (
    StringField,
    PasswordField,
    HiddenField,
    SubmitField,
)
from wtforms import ValidationError, validators as v

from aarau.views.form import (
    SecureForm,
    FailureForm,
    build_form,
    PASSWORD_PATTERN,
)


class ChangePasswordFormBase(SecureForm):
    current_password = PasswordField('Current password', [
        v.Required(),
        v.Length(min=8, max=32),
    ])
    new_password = PasswordField('New password', [
        v.Required(),
        v.Regexp(PASSWORD_PATTERN),
        v.Length(min=8, max=32),
    ])
    new_password_confirmation = PasswordField('Password confirmation', [
        v.Required(),
        v.EqualTo('new_password', message='Passwords must match'),
    ])
    submit = SubmitField('Change')


class ChangePasswordForm(ChangePasswordFormBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._user = None

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, user):
        self._user = user

    def validate_new_password(self, field):  # pylint: disable=no-self-use
        encrypted = self.user.__class__.encrypt_password(field.data)
        if self.user.password == encrypted:
            raise ValidationError(
                'New password is same as current password')


def build_change_password_form(request, user):
    form = build_form(ChangePasswordForm, request)
    form.user = user
    return form


class NewEmailFormBase(SecureForm):
    new_email = StringField('New Email', [
        v.Required(),
        v.Length(min=6, max=64),
        v.Email(),
    ])
    submit = SubmitField('Add')

    def validate_new_email(self, field):
        raise NotImplementedError


class NewEmailForm(NewEmailFormBase):
    def validate_new_email(self, field):
        from aarau.models.user_email import UserEmail

        user_email = UserEmail.select().where(
            UserEmail.email == field.data).first()
        if user_email:
            raise ValidationError('Email is already registered.')


def build_new_email_form(request):
    return build_form(NewEmailForm, request)


class EmailFormBase(SecureForm):
    email = HiddenField('Email', [
        v.Required(),
        v.Length(min=6, max=64),
        v.Email(),
    ])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._user_email = None

    @property
    def user_email(self):
        return self._user_email

    @user_email.setter
    def user_email(self, user_email):
        self._user_email = user_email

    def validate_email(self, field):
        raise NotImplementedError


class DeleteEmailForm(EmailFormBase):
    def validate_email(self, field):
        if not self.user_email:
            raise ValidationError()


def build_delete_email_form(request, user_email):
    if not user_email or user_email.type == 'primary':
        return build_form(FailureForm, request)

    form = build_form(DeleteEmailForm, request)
    form.user_email = user_email
    return form


class ChangeEmailForm(EmailFormBase):
    def validate_email(self, field):
        if not self.user_email:
            raise ValidationError()


def build_change_email_form(request, user_email):
    if not user_email or user_email.activation_state == 'pending' or \
       user_email.type == 'primary':
        return build_form(FailureForm, request)

    form = build_form(ChangeEmailForm, request)
    form.user_email = user_email
    return form
