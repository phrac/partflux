from django.core.exceptions import ObjectDoesNotExist
from django.db import connection
from django import db
from companies.models import Company, CompanyAltName
from parts.models import Part
from distributors.models import Distributor, DistributorSKU
import nltk.data

class Offer:
    def __init__(self, network, product):
        if network == 'cj':
            mapping = {'buylink': 'BUYURL', 'mpn': 'MANUFACTURERID',
                       'manufacturer': 'MANUFACTURER', 'sku': 'SKU',
                       'distributor': 'PROGRAMNAME', 'description': 'NAME',
                       'long_description': 'DESCRIPTION', 'price':'PRICE',
                       'image_url': 'IMAGEURL'}
        elif network == 'pj':
            mapping = {'buylink': 'buy_url', 'mpn': 'mpn', 'upc': 'upc',
                       'manufacturer': 'manufacturer', 'sku': 'sku',
                       'distributor': 'program_name', 'description': 'name',
                       'long_description': 'description_long', 'price':'price',
                       'image_url': 'image_url'}
        else:
            pass
                
        for k, v in mapping.iteritems():
            setattr(self, k, product[v].strip())
            
        self._upcase()
        """
        Clean up the description a bit
        """
        tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        desc = self.long_description.replace(".Product", ". Product")
        desc = desc.replace(".. ", ". ")
        desc = tokenizer.tokenize(desc)
        """
        Advance auto likes to put their marketing into the last sentence of
        the description. Get rid of it.
        """
        if self.distributor == 'Advance Auto Parts':
            desc.pop()
        if self.distributor == 'Auto Parts Warehouse' and len(desc) > 6:
            for x in range(0,6):
                desc.pop()
        self.long_description = ""
        for d in desc:
            if d.startswith("Product Features"):
                pass
            else:
                self.long_description += "%s " % d
        
    def _upcase(self):
        """
        upper() fields needed for the db
        """
        self.manufacturer = self.manufacturer.upper()
        self.mpn = self.mpn.upper()
        self.description = self.description.upper()
        self.sku = self.sku.upper()
        
    
    def populate_db(self):
        distributor = Distributor.objects.get(affiliate_identifier=self.distributor)
        """
        Find the manufacturer of the part or create it if it doesn't exist
        """
        manufacturer = None
        try:
            clookup = CompanyAltName.objects.get(name=self.manufacturer)
            manufacturer = clookup.company
        except:
            pass

        if not manufacturer:
            manufacturer, created = Company.objects.get_or_create(name=self.manufacturer)
        
        """ 
        Get or create the actual manufacturer part
        """
        try:
            part = Part.objects.get(company=manufacturer,
                                    number=self.mpn)
            if part.redirect_part:
                part = part.redirect_part
            if not part.long_description:
                part.long_description = self.long_description
                part.save()
            if not part.image_url:
                part.image_url = self.image_url
                part.save()
        except ObjectDoesNotExist:
            part = Part(number=self.mpn, company=manufacturer,
                        description=self.description, long_description=self.long_description)
            part.save()
        
        """
        See if there is already a SKU for this distributor/part combo
        """
        try:
            distributor_sku = DistributorSKU.objects.get(distributor=distributor,
                                       sku=self.sku)
        except ObjectDoesNotExist:
            distributor_sku = DistributorSKU(sku=self.sku, distributor=distributor, part=part)
        
        distributor_sku.price = self.price
        distributor_sku.affiliate_url = self.buylink
        
        try:
            distributor_sku.save()
        except:
            connection._rollback()

        """ Clear some memory """
        db.reset_queries()
