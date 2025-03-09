# core/jobs.py

from django_apscheduler.jobstores import DjangoJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from django.utils import timezone
from .models import ReserveParking

def deactivate_expired_reservations():
    now = timezone.now()  # Get the current time

    expired_reservations = ReserveParking.objects.filter(
        end_time__lte=now,
        status=True
    )

    for reservation in expired_reservations:
        reservation.status = False
        reservation.save()

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")
    scheduler.add_job(deactivate_expired_reservations, 'interval', minutes=1, name='deactivate_reservations', jobstore='default') # adjust minutes as needed.
    scheduler.start()