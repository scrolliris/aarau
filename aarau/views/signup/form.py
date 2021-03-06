from datetime import datetime

from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    ValidationError,
    validators as v
)

from aarau.views.form import (
    USERNAME_PATTERN,
    USERNAME_PATTERN_INVALID,
    PASSWORD_PATTERN,
    SecureForm,
    build_form,
    availability_checker,
)


def validate_username_uniqueness(_form, field):
    """Unique username check in db."""
    from ...models.user import User
    user = User.select().where(
        User.username == field.data).first()
    if user:
        raise ValidationError('This username is already taken')


def validate_email_uniqueness(_form, field):
    """Unique email address check in db."""
    from ...models.user_email import UserEmail
    user_email = UserEmail.select().where(
        (UserEmail.email == field.data) &
        ((UserEmail.activation_token_expires_at >= datetime.utcnow()) |
         (UserEmail.activation_state == 'active'))).first()
    if user_email:
        raise ValidationError('The email address is already registered')


def username_availability_check(form, field):
    checker = availability_checker('user.username')
    return checker(form, field)


class SignupForm(SecureForm):
    email = StringField('signup.label.email', [
        v.Required(),
        v.Length(min=6, max=64),
        v.Email(),
        validate_email_uniqueness,
    ])
    name = StringField('signup.label.name', [
        v.Optional(),
        v.Length(min=4, max=32),
    ])
    username = StringField('signup.label.username', [
        v.Optional(),
        v.Regexp(USERNAME_PATTERN, message=(
            'You must use only lowercase alphanumeric characters, and '
            'start with a-z'
        )),
        v.Regexp(USERNAME_PATTERN_INVALID),
        v.Length(min=4, max=16),
        validate_username_uniqueness,
        username_availability_check,
    ])
    password = PasswordField('signup.label.password', [
        v.Required(),
        v.Regexp(PASSWORD_PATTERN),
        v.Length(min=8, max=32)
    ])
    submit = SubmitField('signup.submit.create')


def build_signup_form(request):
    return build_form(SignupForm, request)
