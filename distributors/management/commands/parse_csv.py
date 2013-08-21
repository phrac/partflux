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
        network = args[0]
        if network == 'cj':
            path = '/usr/home/vftp/derek/cj'
        if network == 'pj':
            path = '/usr/home/vftp/derek/pj'
        for file in os.listdir(path):
            current_file = os.path.join(path, file)
            counter = 0
            csvfile = csv.DictReader(gzip.open(current_file, 'rb'), delimiter=',')
            for product in csvfile:
                #print product
                offer = Offer(network, product)
                if len(offer.mpn) < 48 and len(offer.mpn) > 2:
                    print "[%s] %s: SKU %s" % (counter, offer.mpn, offer.sku)
                    offer.populate_db()
                    counter += 1
                else:
                    print "INVALID MPN"
            os.remove(current_file)





            
