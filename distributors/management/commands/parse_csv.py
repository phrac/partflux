from django.core.management.base import BaseCommand, CommandError
import csv
from offer import Offer

class Command(BaseCommand):
    args = '<network code> <pj_xml_product_catalog_file.xml>'
    help = 'Parses a product catalog csv file and updates distributor pricing'
    can_import_settings = True
    
    def handle(self, *args, **options):
        counter = 0
        network = args[0]
        file = args[1]
        csvfile = csv.DictReader(open(file, 'rb'), delimiter=',')
        for product in csvfile:
            offer = Offer(network, product)
            print "[%s] %s : %s" % (counter, offer.mpn, offer.description)
            #offer.populate_db()
            counter += 1
            





            
