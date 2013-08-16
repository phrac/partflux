from django.core.management.base import BaseCommand, CommandError
from lxml import etree
from offer import Offer

        
    

class Command(BaseCommand):
    args = '<cj_xml_product_catalog_file.xml>'
    help = 'Parses a CJ product catalog XML file and updates distributor pricing'
    can_import_settings = True
    
    def handle(self, *args, **options):
        product = {}
        counter = 0

        context = etree.iterparse(args[0], events=("start", "end"))
        context = iter(context)
        event, root = context.next()
        
        for event, element in context:
            tag = element.tag
            if element.text:
                product[tag] = element.text
            if event == "end" and element.tag == "product":
                """
                We have reached the last element, process it
                """
                if product:
                    offer = Offer('cj', product)
                    print "[%s] %s : %s" % (counter, offer.mpn, offer.description)
                    offer.populate_db()
                    #populate_db(offer, counter)
                    counter += 1
                    
                product = {}
                root.clear()




            
