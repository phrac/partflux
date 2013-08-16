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
            mapping = {'buylink': 'buyurl', 'mpn': 'manufacturerid',
                       'manufacturer': 'manufacturer', 'sku': 'sku',
                       'distributor': 'programname', 'description': 'name',
                       'long_description': 'description', 'price':'price'}
            
            for k, v in mapping.iteritems():
                setattr(self, k, product[v].strip())
                
            self._upcase()
            """
            Clean up the description a bit
            """
            tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
            desc = self.description.replace(".Product", ". Product")
            desc = tokenizer.tokenize(desc)
            
            """
            Advance auto likes to put their marketing into the last sentence of
            the description. Get rid of it.
            """
            if self.distributor == 'Advance Auto Parts':
                desc.pop()
            description = ""
            for d in desc:
                if d.startswith("Product Features"):
                    pass
                else:
                    description += "%s " % d
            #print description
        
    def _upcase(self):
        """
        upper() fields needed for the db
        """
        self.manufacturer = self.manufacturer.upper()
        self.mpn = self.mpn.upper()
        self.description = self.description.upper()
        self.sku = self.sku.upper()
        
    
    def populate_db(self):
        if len(self.manufacturer) > 48:
            pass
        else:
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
                if not part.long_description:
                    part.long_description = description
                    part.save()
            except ObjectDoesNotExist:
                part = Part(number=self.manufacturer, company=manufacturer,
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