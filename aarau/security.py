from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from .models.user import User


class AuthenticationPolicy(AuthTktAuthenticationPolicy):
    def authenticated_userid(self, req):
        user = req.user
        if user is not None:
            return user.id


def current_user(req):
    user_id = req.unauthenticated_userid
    if user_id is not None:
        try:
            with req.db.atomic():
                user = User.select().where(
                    User.id == user_id,
                    User.activation_state == 'active').get()
            return user
        except:
            return None


def includeme(config):
    settings = config.get_settings()
    config.set_authorization_policy(ACLAuthorizationPolicy())

    auth_policy = AuthenticationPolicy(settings['auth.secret'],
                                       hashalg='sha512')
    config.set_authentication_policy(auth_policy)

    config.add_request_method(current_user, 'user', reify=True)
