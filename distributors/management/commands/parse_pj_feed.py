from django.core.management.base import BaseCommand, CommandError
import csv
from offer import Offer

class Command(BaseCommand):
    args = '<pj_xml_product_catalog_file.xml>'
    help = 'Parses a PepperJam product catalog csv file and updates distributor pricing'
    can_import_settings = True
    
    def handle(self, *args, **options):
        counter = 0

        csvfile = csv.DictReader(open(args[0], 'rb'), delimiter=',')
        for product in csvfile:
            offer = Offer('pj', product)
            print "[%s] %s : %s" % (counter, offer.mpn, offer.description)
            offer.populate_db()
            counter += 1
            





            
