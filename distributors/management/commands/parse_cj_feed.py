from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from django.db import connection
from companies.models import Company, CompanyAltName
from parts.models import Part
from distributors.models import Distributor, DistributorSKU
import xml.etree.cElementTree as etree
#import cElementTree as etree
from xml.parsers import expat

class Command(BaseCommand):
    args = '<cj_xml_product_catalog_file.xml>'
    help = 'Parses a CJ product catalog XML file and updates distributor pricing'
    can_import_settings = True
    
    def handle(self, *args, **options):
        elements = set(['product'])
        child_elements = set(['programname', 'manufacturer', 'manufacturerid',
                              'name', 'sku', 'price', 'buyurl'])

        offer = {}
        counter = 0

        context = etree.iterparse(args[0], events=("start", "end"))
        
        for event, element in context:
            tag = element.tag
            if tag in child_elements:
                if element.text:
                    offer[tag] = element.text
            elif tag in elements:
                """
                We have reached the last element, process it
                """
                if offer:
                    #print offer
                    populate_db(offer, counter)
                    counter += 1
                    #print counter
                    offer = {}
                    #element.clear()
            

def populate_db(offer, counter):
    if len(offer['manufacturerid']) > 48:
        pass
    else:
        manufacturer = None
        try:
            clookup = CompanyAltName.objects.get(name=offer['manufacturer'].upper())
            manufacturer = clookup.company
        except:
            pass

        distributor = Distributor.objects.get(affiliate_identifier=offer['programname'])
        
        if not manufacturer:
            try:
                manufacturer = Company.objects.get(name=offer['manufacturer'].upper())
            except ObjectDoesNotExist:
                manufacturer = Company(name=offer['manufacturer'].upper())
                manufacturer.save()
        try:
            part = Part.objects.get(company=manufacturer,
                                    number=offer['manufacturerid'].upper())
        except ObjectDoesNotExist:
            part = Part(number=offer['manufacturerid'].upper(), company=manufacturer,
                        description=offer['name'].upper())
            part.save()
        try:
            distributor_sku = DistributorSKU.objects.get(distributor=distributor,
                                       sku=offer['sku'].upper())
        except ObjectDoesNotExist:
            distributor_sku = DistributorSKU(sku=offer['sku'].upper(), distributor=distributor, part=part)
        
        distributor_sku.price = offer['price']
        distributor_sku.affiliate_url = offer['buyurl']
        
        try:
            distributor_sku.save()
        except:
            connection._rollback()
        
    print ('[%s] %s : %s' % (counter, offer['manufacturer'],
                                   offer['manufacturerid']))
            
