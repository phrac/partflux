from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.template.defaultfilters import slugify
from django.utils.encoding import smart_str
from sorl.thumbnail import ImageField
from amazon.api import AmazonAPI
from django_hstore import hstore

import itertools

from companies.models import Company

class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)
    slug = models.CharField(max_length=128, null=True, blank=True)
    parent = models.ForeignKey('Category', null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super(Category, self).save(*args, **kwargs)

    def get_taxonomy(self):
        parents = []
        p = self
        while p is not None:
            parents.append(p)
            p = p.parent

        return list(reversed(parents))

    def get_children(self):
        return Category.objects.filter(parent=self).order_by(name)

    def get_required_keys(self):
        keys = []
        parents = self.get_taxonomy()
        for p in parents:
            props = CategoryProperty.objects.filter(category=p)
            for k in props:
                if k.required_key is True:
                    keys.append(k.key_name)
        return keys



class CategoryProperty(models.Model):
    """
    This is a model that will define the properties stored for each part.
    """
    category = models.ForeignKey(Category)
    key_name = models.CharField(max_length=16)
    required_key = models.BooleanField(default=False)

    class Meta:
        unique_together = ('category', 'key_name',)
        verbose_name_plural = 'Category Properties'

    def __unicode__(self):
        return self.key_name


class Part(models.Model):
    number = models.CharField(max_length=48)
    category = models.ForeignKey(Category, null=True)
    slug = models.CharField(max_length=64)
    description = models.TextField(null=False)
    long_description = models.TextField(null=True, blank=True)
    company = models.ForeignKey(Company)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    images = models.ManyToManyField('PartImage')
    image_url = models.URLField(max_length=512, null=True)
    asin = models.CharField(max_length=10, null=True, blank=True)
    upc = models.CharField(max_length=13, null=True, blank=True)
    ean = models.CharField(max_length=13, null=True, blank=True)
    properties = hstore.DictionaryField(null=True, blank=True)
    cross_references = models.ManyToManyField('Part', related_name='xrefs')

    objects = hstore.HStoreManager()

    class Meta:
        unique_together = ('number', 'company',)
    
    def __unicode__(self):
        return self.number

    def save(self, *args, **kwargs):
        self.number = self.number.strip().upper()
        self.description = self.description.strip().upper()
        if not self.slug:
            self.slug = slugify(self.number)

        if not self.properties:
            self.properties = dict(itertools.izip_longest(*[iter(self.category.get_required_keys())] * 2, fillvalue=""))

        super(Part, self).save(*args, **kwargs)

    def get_alternates(self):
        alternates = []
        parts = Part.objects.filter(redirect_part=self)
        for p in parts:
            alternates.append(p.number)
        return alternates
        
    @property
    def amazon_keywords(self):
        term = self.number
        for x in self.cross_references.all():
            term += " %s" % x.number
        return term
    
    def amazon_price(self):
        amazon = AmazonAPI(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY, settings.AWS_ASSOCIATE_TAG)
        try:
            product = amazon.lookup(ItemId=self.asin)
            price = product.price_and_currency
            return "$%.2f %s" % (price[0], price[1])
        except:
            return None

    def asin_thumbnail(self):
        amazon = AmazonAPI(settings.AWS_ACCESS_KEY_ID,
                           settings.AWS_SECRET_ACCESS_KEY,
                           settings.AWS_ASSOCIATE_TAG)
        try:
            product = amazon.lookup(ItemId=self.asin)
            return product.medium_image_url
        except:
            return None

    def asin_image(self): 
        amazon = AmazonAPI(settings.AWS_ACCESS_KEY_ID,
                           settings.AWS_SECRET_ACCESS_KEY,
                           settings.AWS_ASSOCIATE_TAG)
        try: 
            product = amazon.lookup(ItemId=self.asin)
            return product.large_image_url
        except:
            return None

    def asin_search(self):
        try:
            amazon = AmazonAPI(settings.AWS_ACCESS_KEY_ID,
                           settings.AWS_SECRET_ACCESS_KEY,
                           settings.AWS_ASSOCIATE_TAG)
            products = amazon.search_n(10, Keywords="%s %s" %
                                       (self.company.name, self.number), SearchIndex='All')
        except:
            products = None
        return products


    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('parts.views.detail', args=[str(self.id), str(self.company.slug),
                                               str(self.slug)])

class Attribute(models.Model):
    part = models.ForeignKey('Part')
    key = models.CharField(max_length=64)
    value = models.CharField(max_length=128)

    class Meta:
        unique_together = ('part', 'key', 'value')
        ordering = ('value',)
        
    def get_attr_string(self):
        return u"%s: %s" % (smart_str(self.key), smart_str(self.value))

    def save(self, *args, **kwargs):
        self.key = self.key.strip().upper()
        self.value = self.value.strip().upper()
        super(Attribute, self).save(*args, **kwargs)

        
class PartImage(models.Model):
    image = ImageField(upload_to='part_images')
    approved = models.BooleanField(default=True)
    album_cover = models.BooleanField(default=False)


