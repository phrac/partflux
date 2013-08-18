from django.core.management.base import BaseCommand, CommandError
import csv
from offer import Offer
import gzip
import os

class Command(BaseCommand):
    args = '<network code> <pj_xml_product_catalog_file.xml>'
    help = 'Parses a product catalog csv file and updates distributor pricing'
    can_import_settings = True
    
    def handle(self, *args, **options):
        path = '/usr/home/vftp/derek/cj'
        for file in os.listdir(path):
            current_file = os.path.join(path, file)
            counter = 0
            network = args[0]
            csvfile = csv.DictReader(gzip.open(current_file, 'rb'), delimiter=',')
            for product in csvfile:
                offer = Offer(network, product)
                print "[%s] %s: SKU %s" % (counter, offer.mpn, offer.sku)
                if len(offer.mpn) < 48:
                    offer.populate_db()
                counter += 1
            os.remove(current_file)





            
