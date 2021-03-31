from django.core.management.base import BaseCommand
from trade_platform.models import User

class Command(BaseCommand):
    """Register new user in system"""
    help = 'python manage.py create_user -u new_username -p new_password'

    def add_arguments(self, parser):
        parser.add_argument(
            '-u',
            '--username',
            action='store',
            help='New user username'
        )

        parser.add_argument(
            '-p',
            '--password',
            action='store',
            help='New user password'
        )

    def handle(self, *args, **options):
        user,_ = User.objects.get_or_create(username=options['username'])
        user.set_password(options['password'])
        user.save()

