import logging
import os

from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_EXECUTED
from apscheduler.schedulers.background import BackgroundScheduler
from django.core.management import call_command

# Logging setup for APScheduler
logger = logging.getLogger(__name__)


def example_schedule():
    # This function will be called by APScheduler
    call_command("example_cron_job")


def start_scheduler():
    # Initialize the scheduler
    scheduler = BackgroundScheduler()

    # Add the job to run daily at midnight (00:00)
    scheduler.add_job(
        example_schedule
    ,
        "cron",
        hour=os.getenv("CRON_JOBS_TIME_HOUR", "00"),
        minute=os.getenv("CRON_JOBS_TIME_MINUTE", "00"),
    )

    # Add event listeners (Optional for logging job events)
    scheduler.add_listener(job_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)

    # Start the scheduler
    scheduler.start()


def job_listener(event):
    if event.exception:
        logger.error(f"Job {event.job_id} failed")
        print(f"Job {event.job_id} failed")
    else:
        logger.info(f"Job {event.job_id} completed successfully")
        print(f"Job {event.job_id} completed successfully")
