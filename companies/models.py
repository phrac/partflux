from django.db import models
from django.template.defaultfilters import slugify
from sorl.thumbnail import ImageField

class Company(models.Model):
    name = models.CharField(max_length=128, unique=True)
    slug = models.CharField(max_length=64, blank=True, unique=True)
    description = models.TextField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    wikipedia_url = models.URLField(null=True, blank=True)
    facebook_url = models.URLField(null=True, blank=True)
    twitter_name = models.CharField(max_length=32, null=True, blank=True)
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
    
    class Meta:
        ordering = ('name',)

    def save(self, *args, **kwargs):
        self.name = self.name.strip().upper()
        self.slug = slugify(self.name)
        super(Company, self).save(*args, **kwargs)

    def __unicode__(self):
        return "%s (%s)" % (self.name, self.id )
    
    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('companies.views.detail', args=[str(self.id),
                                                       str(self.slug)])

class CompanyAltName(models.Model):
    company = models.ForeignKey(Company)
    name = models.CharField(max_length=128, unique=True)
    
    class Meta:
        ordering = ('company',)

    def __unicode__(self):
        return "%s : Real Name: %s" % (self.name, self.company.name)
