from django.db import models
from django.contrib.auth.models import User
from django.contrib.comments.moderation import CommentModerator, moderator
from django.template.defaultfilters import slugify
from django.conf import settings
from django_orm.postgresql import hstore
from sorl.thumbnail import ImageField

from companies.models import Company
from nsn.models import Nsn
from pyes import *

class Part(models.Model):
    """
    Stores a unique part number and related information

    """
    number = models.CharField(max_length=48)
    slug = models.CharField(max_length=64)
    description = models.TextField()
    company = models.ForeignKey(Company)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, null=True)
    hits = models.IntegerField(default=0, editable=False)
    approved = models.BooleanField(default=True)
    nsn = models.ForeignKey(Nsn, null=True)
    images = models.ManyToManyField('PartImage')
    source = models.URLField()
    attributes = hstore.DictionaryField()

    objects = hstore.HStoreManager()
    
    def __unicode__(self):
        return self.number

    class Meta:
        unique_together = ('number', 'company',)

    def save(self, *args, **kwargs):
        """
        Slugify the part number and upcase the number and description. Also
        updates the ElasticSearch index.

        """
        self.number = self.number.strip().upper()
        self.description = self.description.strip().upper()
        self.slug = slugify(self.number)
        self.update_ES()
        super(Part, self).save(*args, **kwargs)
    
    def update_ES(self):
        """ 
        Update the ElasticSearch index with fresh data about the part.
        
        """
        es = ES(settings.ES_HOST)
        attrlist, attrstring = self.prepare_attrs()
        es.index(
        {
            "pgid" : self.id, 
            "number" : self.number, 
            "company" : self.company.name, 
            "attrstring" : attrstring,
            "desc" : self.description,
            "attributes" : attrlist,
        }, 
        "parts", "part-type", self.id
        )
        es.refresh('parts')
    
    def prepare_attrs(self):
        """
        Turn the hstore attribute column into a dict & string for storage in
        ElasticSearch

        """
        attrlist = []
        attrstring = ''
        for k, v in self.attributes.iteritems():
            attr = {}
            vals = v.split("|")
            attr['key'] = k
            attr['values'] = vals
            attrlist.append(attr)
            attrstring += "%s " % k
            attrstring += "%s " % v.replace('|', '')

        return attrlist, attrstring
    
    def save_attributes(self, k, v):
        """
        Multiple values are stored in the PostgreSQL hstore column `attributes`.
        We have to marshal and unmarshal this column to check for duplicates and
        add new attributes.

        """
        keys = []
        cleankey = k.strip().upper()
        cleanvalue = v.strip().upper()
        for key, value in self.attributes.iteritems():
            keys.append(key)
        if cleankey not in keys:
            self.attributes[cleankey] = cleanvalue
            status = True
        else:
            valuestring = self.attributes[k]
            values = valuestring.split("|")
            if cleanvalue in values:
               status = False 
            else:
                valuestring = valuestring + "|%s" % cleanvalue
                self.attributes[cleankey] = valuestring
                status = True
        self.save()
        return status

    
    @models.permalink
    def get_absolute_url(self):
        return ('parts.views.detail', [str(self.company.slug), str(self.slug)])

class Xref(models.Model):
    """ Store part number cross references, related to :model:`parts.Part` and
    :model:`auth.User`.

    """
    user = models.ForeignKey(User, null=True)
    part = models.ForeignKey('Part')
    xrefpart = models.ForeignKey('Part', related_name='xrefpart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)

    class Meta:
        unique_together = ('part', 'xrefpart',)

class PartImage(models.Model):
    image = ImageField(upload_to='part_images')
    user = models.ForeignKey(User, null=False)
    approved = models.BooleanField(default=True)
    album_cover = models.BooleanField(default=False)
    
class BuyLink(models.Model):
    part = models.ForeignKey('Part')
    company = models.ForeignKey(Company)
    url = models.URLField(null=False)
    price = models.DecimalField(max_digits=16, decimal_places=4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    link_ok = models.BooleanField(default=True)
    price_xpath = models.CharField(max_length=512, null=True, blank=True)

    class Meta:
        unique_together = ('part', 'company')


class PartModerator(CommentModerator):
    email_notification = True

moderator.register(Part, PartModerator)


