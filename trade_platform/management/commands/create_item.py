from django.core.management.base import BaseCommand
from trade_platform.models import Item

class Command(BaseCommand):
    """Can add new item object in system"""
    help = 'python manage.py create_item -c new_item_code -n new_item_name'

    def add_arguments(self, parser):
        parser.add_argument(
            '-c',
            '--code',
            action='store',
            help='Item code'
        )

        parser.add_argument(
            '-n',
            '--name',
            action='store',
            help='Item name'
        )

    def handle(self, *args, **options):
        item,_ = Item.objects.get_or_create(name=options['name'], code=options['code'])
        item.save()

