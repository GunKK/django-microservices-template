import os

from celery import Celery
from celery.utils.log import get_task_logger
from django.core.mail import BadHeaderError
from django.core.management import call_command
from dotenv import load_dotenv

from core.mail import MailService

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")

load_dotenv()
logger = get_task_logger(__name__)

CELERY_BROKER_URL = os.getenv("CELERY_REDIS_URL", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND = os.getenv("CELERY_REDIS_URL", "redis://localhost:6379/0")

app = Celery(
    __name__,
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
)

# Automatically discover tasks in all registered Django app configs
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


@app.task(name="send_email_task", bind=True, max_retries=3)
def send_email_task(self, user_email, otp):
    try:
        logger.info("send mail task")
        MailService.send_verify_otp(user_email, otp)
    except BadHeaderError:
        logger.info("BadHeaderError")
    except Exception as e:
        logger.error("error exception")
        logger.error(e)


@app.task(name="send_email_password_reset", bind=True, max_retries=3)
def send_email_password_reset(self, user, domain, uid, token, protocol):
    try:
        logger.info("send mail reset password")
        MailService.send_password_reset_link(user, domain, uid, token, protocol)
    except BadHeaderError:
        logger.info("BadHeaderError")
    except Exception as e:
        logger.error("error exception")
        logger.error(e)


@app.task(name="send_mail_active_account_success", bind=True, max_retries=3)
def send_mail_active_account(self, user, domain, protocol):
    try:
        logger.info("mail active account")
        MailService.active_account_success(user, domain, protocol)
    except BadHeaderError:
        logger.info("BadHeaderError")
    except Exception as e:
        logger.error("error exception")
        logger.error(e)


@app.task(name="update_project_status", bind=True, max_retries=3)
def update_project_status(self):
    logger.info("BadHeaderError")
    call_command("update_project_status_command")


@app.task(name="update_task_status", bind=True, max_retries=3)
def update_task_status(self):
    call_command("update_task_status_command")


@app.task(name="update_start_task", bind=True, max_retries=3)
def update_start_task(self):
    call_command("update_start_task_command")


@app.task(name="send_mail_request_active_account", bind=True, max_retries=3)
def send_mail_request_active_account(self, user_admin, domain, user, protocol):
    try:
        logger.info("mail active account")
        MailService.request_active_account(user_admin, domain, user, protocol)
    except BadHeaderError:
        logger.info("BadHeaderError")
    except Exception as e:
        logger.error("error exception")
        logger.error(e)
