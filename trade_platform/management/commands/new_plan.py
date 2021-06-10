from django.core.management.base import BaseCommand

from trade_platform.services.create_test_data import ShiftPlanCreator


class Command(BaseCommand):
    """
    Add 3 workshift plans, witch 10, 20, 50 workshifts
    """
    help = 'python manage.py new_plan'

    def add_arguments(self, parser):
        parser.add_argument(
            '-a',
            '--amount',
            action='store',
            help='Amount of positions to add in database'
        )

    def handle(self, *args, **options):
        ShiftPlanCreator.create_test_data(options['amount'])
