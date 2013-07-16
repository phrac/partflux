from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.template.defaultfilters import slugify
from django.utils.encoding import smart_str
from sorl.thumbnail import ImageField

from companies.models import Company
from nsn.models import Nsn

class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)
    slug = models.CharField(max_length=128)
    parent = models.ForeignKey('Category', null=True)
    
class Part(models.Model):
    number = models.CharField(max_length=48)
    categories = models.ManyToManyField(Category, related_name='part_category')
    slug = models.CharField(max_length=64)
    description = models.TextField(null=False)
    company = models.ForeignKey(Company)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, null=True)
    hits = models.IntegerField(default=0, editable=False)
    approved = models.BooleanField(default=True)
    nsn = models.ForeignKey(Nsn, null=True)
    images = models.ManyToManyField('PartImage')
    asin = models.CharField(max_length=10)
    cross_references = models.ManyToManyField('Part', related_name='xrefs')

    def __unicode__(self):
        return self.number

    class Meta:
        unique_together = ('number', 'company',)

    def save(self, *args, **kwargs):
        self.number = self.number.strip().upper()
        self.description = self.description.strip().upper()
        if not self.slug:
            self.slug = slugify(self.number)
        super(Part, self).save(*args, **kwargs)
           
    @models.permalink
    def get_absolute_url(self):
        return ('parts.views.detail', [self.id, str(self.company.slug), str(self.slug)])

class Attribute(models.Model):
    part = models.ForeignKey('Part')
    key = models.CharField(max_length=64)
    value = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, null=True)
    upvotes = models.IntegerField(null=True, default=0)
    downvotes = models.IntegerField(null=True, default=0)

    class Meta:
        unique_together = ('part', 'key', 'value')
        ordering = ('value',)
        
    def get_attr_string(self):
        return u"%s: %s" % (smart_str(self.key), smart_str(self.value))

    def save(self, *args, **kwargs):
        self.key = self.key.strip().upper()
        self.value = self.value.strip().upper()
        super(Attribute, self).save(*args, **kwargs)
        
    def get_flags():
        return Attribute.objects.get(attribute=self)


class PartImage(models.Model):
    image = ImageField(upload_to='part_images')
    user = models.ForeignKey(User, null=False)
    hash = models.CharField(max_length=1000, unique=True)
    approved = models.BooleanField(default=True)
    album_cover = models.BooleanField(default=False)


