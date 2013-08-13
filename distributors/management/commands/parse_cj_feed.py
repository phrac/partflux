from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from django.db import connection
from companies.models import Company
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
        
        doc = etree.parse(args[0], recover=True)
        root = doc.getroot()
        products = doc.findall('product')
        for product in products:
            aid = product.find('programname').text
            mfg = product.find('manufacturer').text.upper()
            mfg_part = product.find('manufacturerid').text.upper()
            desc = product.find('name').text.upper()
            sku = product.find('sku').text
            price = product.find('saleprice').text.replace(',', '')
            affiliate_url = product.find('buyurl').text
            if len(mfg_part) > 48:
                pass
            else:
                distributor = Distributor.objects.get(affiliate_identifier=aid)
                try:
                    manufacturer = Company.objects.get(name=mfg.upper())
                except ObjectDoesNotExist:
                    manufacturer = Company(name=mfg.upper())
                    manufacturer.save()
                try:
                    part = Part.objects.get(company=manufacturer, number=mfg_part.upper())
                except ObjectDoesNotExist:
                    part = Part(number=mfg_part, company=manufacturer, description=desc)
                    part.save()
                try:
                    distributor_sku = DistributorSKU.objects.get(distributor=distributor, sku=sku)
                except ObjectDoesNotExist:
                    distributor_sku = DistributorSKU(sku=sku, distributor=distributor, part=part)
                
                distributor_sku.price = price
                distributor_sku.affiliate_url = affiliate_url
                
                try:
                    distributor_sku.save()
                except:
                    connection._rollback()
                
            self.stdout.write('%s : %s' % (mfg, mfg_part))
            break
            
        
    