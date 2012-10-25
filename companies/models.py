from django.db import models
from django.template.defaultfilters import slugify
from sorl.thumbnail import ImageField
from pyes import *

class Company(models.Model):
    name = models.CharField(max_length=128, unique=True)
    slug = models.CharField(max_length=64, blank=True)
    description = models.TextField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    wikipedia_url = models.URLField(null=True, blank=True)
    facebook_url = models.URLField(null=True, blank=True)
    twitter_url = models.URLField(null=True, blank=True)
    linkedin_url = models.URLField(null=True, blank=True) 
    email = models.EmailField(max_length=32, null=True, blank=True)
    phone = models.CharField(max_length=16, null=True, blank=True)
    fax = models.CharField(max_length=16, null=True, blank=True)
    address1 = models.CharField(max_length=64, null=True, blank=True)
    address2 = models.CharField(max_length=64, null=True, blank=True)
    city = models.CharField(max_length=32, null=True, blank=True)
    state = models.CharField(max_length=32, null=True, blank=True)
    zip = models.CharField(max_length=10, null=True, blank=True)
    country = models.CharField(max_length=32, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    logo = ImageField(upload_to='company_logos', null=True, blank=True)

    def save(self, *args, **kwargs):
        self.name = self.name.strip().upper()
        self.slug = slugify(self.name)
        super(Company, self).save(*args, **kwargs)
        #self.update_ES()

    def __unicode__(self):
        return self.name
    
    """ Update the ElasticSearch index """
    def update_ES(self):
        es = ES('127.0.0.1:9200')
        es.index(
            {
                "pgid" : str(self.id), 
                "company_name" : self.name, 
            }, 
            "companies", "company-type", self.id
        )
        es.refresh('companies')

    @models.permalink
    def get_absolute_url(self):
        return ('companies.views.detail', [str(self.slug)])

class CompanyContact(models.Model):
    SEX = (('M', 'Male'),
           ('F', 'Female'))

    company = models.ForeignKey('Company')
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    sex = models.CharField(max_length=1, choices=SEX)
    email = models.EmailField()
    work_phone = models.CharField(max_length=16)
    cell_phone = models.CharField(max_length=16)
    fax = models.CharField(max_length=16)

    class Meta:
        unique_together = ('company', 'first_name', 'last_name',)
    
class CompanyBranch(models.Model):
    company = models.ForeignKey('Company')
    name = models.CharField(max_length=32)
    email = models.EmailField(max_length=32)
    phone = models.CharField(max_length=16)
    fax = models.CharField(max_length=16)
    address1 = models.CharField(max_length=64)
    address2 = models.CharField(max_length=64)
    city = models.CharField(max_length=32)
    state = models.CharField(max_length=32)
    country = models.CharField(max_length=32)
    zip = models.CharField(max_length=8)
