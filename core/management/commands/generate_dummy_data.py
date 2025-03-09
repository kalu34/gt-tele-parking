import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from authentication.models import User
from core.models import Payment, ApprovedRequest
from django.utils.timezone import make_aware

class Command(BaseCommand):
    help = 'Generate 100 dummy Payment objects'

    def handle(self, *args, **kwargs):
        statuses = ['pending', 'successful', 'failed']
        currency = 'ETB'

        # Get the single ApprovedRequest object
        approved_request = ApprovedRequest.objects.first()
        if not approved_request:
            self.stdout.write(self.style.ERROR("No ApprovedRequest object found. Please create one before running this script."))
            return

        # Get all users
        users = list(User.objects.all())
        if not users:
            self.stdout.write(self.style.ERROR("Please ensure you have User objects in your database."))
            return

        for _ in range(100):
          user = random.choice(users)
          tx_ref = f"TX-{random.randint(100000, 999999)}"
          amount = round(random.uniform(50.0, 1000.0), 2)
          status = "successful"
          random_date = datetime.now() - timedelta(days=random.randint(0, 365))

          # Create payment with default date
          payment = Payment.objects.create(
              request_id=approved_request,
              tx_ref=tx_ref,
              user=user,
              amount=amount,
              currency=currency,
              status=status,
          )

          # Update the date field
          payment.date = make_aware(random_date)  # Make the datetime timezone-aware
          payment.save()

        self.stdout.write(self.style.SUCCESS("100 dummy payments created successfully."))
