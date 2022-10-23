import json
from django.core.management.base import BaseCommand
from core.utils import import_legacy


class Command(BaseCommand):
    help = 'Loads reading data from a legacy JSON dump'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str)

    def handle(self, *args, **options):
        js = json.load(open(options['json_file'], 'r'))
        import_legacy(js)
        self.stdout.write(self.style.SUCCESS("Imported books and updates"))
