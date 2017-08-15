from contextlib import contextmanager

from . import blank_request, worker
from ..mailers.user_mailer import UserMailer


@contextmanager
def _db():
    from .. import get_settings
    from ..models import init_db

    settings = get_settings()
    db = init_db(settings)

    if db.is_closed():
        db.connect()

    yield db

    if not db.is_closed():
        db.close()


class SendEmailTask(worker.Task):
    queue = 'default'

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print('{0!r} failed: {1!r}'.format(task_id, exc))


@worker.task(base=SendEmailTask, autoretry_for=(Exception,),
             retry_kwargs={'max_retries': 3})
def send_account_activation_email(user_email_id):
    with _db() as db, db.atomic():
        from ..models.user_email import UserEmail

        user_email = UserEmail.select().where(
            UserEmail.id == user_email_id).get()

        mailer = UserMailer(blank_request())
        mailer.account_activation_email(user_email).deliver()


@worker.task(base=SendEmailTask, autoretry_for=(Exception,),
             retry_kwargs={'max_retries': 3})
def send_email_activation_email(user_email_id):
    with _db() as db, db.atomic():
        from ..models.user_email import UserEmail

        user_email = UserEmail.select().where(
            UserEmail.id == user_email_id).get()

        mailer = UserMailer(blank_request())
        mailer.email_activation_email(user_email).deliver()


@worker.task(base=SendEmailTask, autoretry_for=(Exception,),
             retry_kwargs={'max_retries': 3})
def send_reset_password_email(user_id):
    from datetime import datetime

    with _db() as db, db.atomic():
        from ..models.user import User

        user = User.select().where(User.id == user_id).get()

        mailer = UserMailer(blank_request())
        mailer.reset_password_email(user).deliver()

        user.reset_password_token_sent_at = datetime.utcnow()
        user.save()
