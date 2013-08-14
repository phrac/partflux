from django.core.management.base import BaseCommand, CommandError
from parts.models import Part
from companies.models import Company
import gc
import datetime

class Command(BaseCommand):
    def handle(self, *args, **options):
        LIMIT = 10
        pk = 0
        parts = Company.objects.filter(created_at__gte=datetime.date.today)[:LIMIT]
        for p in parts:
            print p
            p.delete()
            gc.collect()

        self.stdout.write("\nFinished.\n")

