from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.comments.moderation import CommentModerator, moderator
from django.template.defaultfilters import slugify
from django.conf import settings
from sorl.thumbnail import ImageField

from companies.models import Company
from nsn.models import Nsn

class Part(models.Model):
    """
    Stores a unique part number and related information

    """
    number = models.CharField(max_length=48)
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
    source = models.URLField()

    def __unicode__(self):
        return self.number

    class Meta:
        unique_together = ('number', 'company',)

    def save(self, *args, **kwargs):
        """
        Slugify the part number and upcase the number and description. 

        """
        self.number = self.number.strip().upper()
        self.description = self.description.strip().upper()
        self.slug = slugify(self.number)
        super(Part, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return ('parts.views.detail', [self.id, str(self.company.slug), str(self.slug)])

class PartFlag(models.Model):
    part = models.ForeignKey('Part')
    user = models.ForeignKey(User)
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField()

class Attribute(models.Model):
    part = models.ForeignKey('Part')
    key = models.CharField(max_length=64)
    value = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, null=True)
    upvotes = models.IntegerField(null=True)
    downvotes = models.IntegerField(null=True)

    class Meta:
        unique_together = ('part', 'key', 'value')
        ordering = ('value',)

    def save(self, *args, **kwargs):
        self.key = self.key.strip().upper()
        self.value = self.value.strip().upper()
        if not self.upvotes:
            self.upvotes = 0
        if not self.downvotes:
            self.downvotes = 0
        super(Attribute, self).save(*args, **kwargs)
        
    def get_flags():
        return Attribute.objects.get(attribute=self)

class AttributeFlag(models.Model):
    attribute = models.ForeignKey('Attribute')
    user = models.ForeignKey(User)
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField()

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


#moderator.register(Part, PartModerator)


