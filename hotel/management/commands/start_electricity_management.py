import datetime
import logging

import pytz
from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django.utils import timezone
from django_apscheduler.jobstores import DjangoJobStore

from hotel.utils.scheduler_triggers import TriggerActions

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            TriggerActions.motion_detection_trigger,
            trigger=CronTrigger(second="*/1"),  # Every 1 seconds
            id="motion_detection_trigger",
            max_instances=1,
            replace_existing=True
        )
        logger.info("Added job 'motion_detection_trigger'.")

        scheduler.add_job(
            TriggerActions.night_shift_start_trigger,
            trigger=CronTrigger(minute=settings.NIGHT_SHIFT_START['minute'],
                                hour=settings.NIGHT_SHIFT_START['hour'],
                                timezone=pytz.timezone(settings.TIME_ZONE)),
            id="night_shift_start_trigger",
            max_instances=1,
            replace_existing=True
        )
        logger.info("Added job 'night_shift_start_trigger'.")

        scheduler.add_job(
            TriggerActions.night_shift_end_trigger,
            trigger=CronTrigger(minute=settings.NIGHT_SHIFT_END['minute'],
                                hour=settings.NIGHT_SHIFT_END['hour'],
                                timezone=pytz.timezone(settings.TIME_ZONE)),
            id="night_shift_end_trigger",
            max_instances=1,
            replace_existing=True
        )
        logger.info("Added job 'night_shift_end_trigger'.")

        scheduler.add_job(
            TriggerActions.delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="12", minute="00"
            ),  # Noon of Monday
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")