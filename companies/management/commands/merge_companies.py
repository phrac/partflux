from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from django.db import connection
from companies.models import Company
from parts.models import Part
from distributors.models import Distributor, DistributorSKU

class Command(BaseCommand):
    args = '<cj_xml_product_catalog_file.xml>'
    help = 'Parses a CJ product catalog XML file and updates distributor pricing'
    can_import_settings = True
    
    def handle(self, *args, **options):
        from_company = args[0]
        to_company = args[1]
        from_c = Company.objects.get(id=from_company)
        to_c = Company.objects.get(id=to_company)

        parts = Part.objects.filter(company=from_c)
        for p in parts:
            print "Processing %s" % p.number
            try:
                finalp = Part.objects.get(company=to_c, number=p.number)
                skus = DistributorSKU.objects.filter(part=p)
                for sku in skus:
                    sku.part=finalp
                    sku.save()
                p.delete()

            except:
                p.company = to_c
                p.save()

        from_c.delete()



