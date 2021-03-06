from contextlib import contextmanager

from aarau.tasks import blank_request, worker
from aarau.mailers.user_mailer import UserMailer


@contextmanager
def _db(db_kind):
    from aarau import get_settings
    from aarau.models import init_db

    settings = get_settings()
    db = init_db(settings, db_kind)

    if db.is_closed():
        db.connect()

    yield db

    if not db.in_transaction() and not db.is_closed():
        db.close()


class SendEmailTask(worker.Task):
    queue = 'default'

    # pylint: disable=no-self-use,too-many-arguments
    def on_failure(self, exc, task_id, _args, _kwargs, _einfo):
        print('{0!r} failed: {1!r}'.format(task_id, exc))


@worker.task(base=SendEmailTask, autoretry_for=(Exception,),
             retry_kwargs={'max_retries': 3})
def send_account_activation_email(user_email_id):
    with _db('cardinal') as db, db.atomic():
        from aarau.models.user_email import UserEmail

        user_email = UserEmail.select().where(
            UserEmail.id == user_email_id).get()

        mailer = UserMailer(blank_request())
        mailer.account_activation_email(user_email).deliver()


@worker.task(base=SendEmailTask, autoretry_for=(Exception,),
             retry_kwargs={'max_retries': 3})
def send_email_activation_email(user_email_id):
    with _db('cardinal') as db, db.atomic():
        from aarau.models.user_email import UserEmail

        user_email = UserEmail.select().where(
            UserEmail.id == user_email_id).get()

        mailer = UserMailer(blank_request())
        mailer.email_activation_email(user_email).deliver()


@worker.task(base=SendEmailTask, autoretry_for=(Exception,),
             retry_kwargs={'max_retries': 3})
def send_reset_password_email(user_id):
    from datetime import datetime

    with _db('cardinal') as db, db.atomic():
        from aarau.models.user import User

        user = User.select().where(User.id == user_id).get()

        mailer = UserMailer(blank_request())
        mailer.reset_password_email(user).deliver()

        user.reset_password_token_sent_at = datetime.utcnow()
        user.save()
