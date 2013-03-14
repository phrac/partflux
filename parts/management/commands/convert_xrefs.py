from django.core.management.base import BaseCommand, CommandError
from parts.models import Part, Xref
import gc

class Command(BaseCommand):
    def handle(self, *args, **options):
        LIMIT = 100
        pk = 0
        i = 0
        last_pk = Xref.objects.all().order_by('-pk')[0].pk

        while pk < last_pk:
            self.stderr.write("%d..." % i)
            for row in Xref.objects.filter(pk__gt=pk)[:LIMIT]:
                pk = row.pk
                row.part.cross_references.add(row.xrefpart)
            gc.collect()
            i += LIMIT

        self.stdout.write("\nFinished.\n")

