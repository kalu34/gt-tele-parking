from django.core.management.base import BaseCommand
from authentication.models import User

class Command(BaseCommand):
    help = "Create a new user with default password '123'"

    def add_arguments(self, parser):
        """Define command-line arguments"""
        parser.add_argument('username', type=str, help="Username for the new user")
        parser.add_argument('first_name', type=str, help="First name of the user")
        parser.add_argument('last_name', type=str, help="Last name of the user")
        parser.add_argument('email', type=str, help="Email of the user")
        parser.add_argument('role', type=str, help="Role of the user")
        parser.add_argument('phone_number', type=str, help="Role of the user")

    def handle(self, *args, **kwargs):
        """Execute the command"""
        username = kwargs['username']
        first_name = kwargs['first_name']
        last_name = kwargs['last_name']
        email = kwargs['email']
        role = kwargs['role']
        phone_number = kwargs['phone_number']

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.ERROR(f"User with username '{username}' already exists."))
            return

        user = User(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            role=role,
            phone_number=phone_number
        )

        user.set_password("123")  # Set password to 123
        user.save()

        self.stdout.write(self.style.SUCCESS(f"User '{username}' created successfully with password '123'!"))
