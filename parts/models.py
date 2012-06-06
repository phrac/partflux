from django.db import models
from django.contrib.auth.models import User
from django.contrib.comments.moderation import CommentModerator, moderator
from sorl.thumbnail import ImageField

from companies.models import Company
from nsn.models import Nsn

class Part(models.Model):
    number = models.CharField(max_length=48)
    slug = modelx.CharField(max_length=64)
    description = models.TextField()
    company = models.ForeignKey(Company)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, null=True)
    hits = models.IntegerField(default=0, editable=False)
    approved = models.BooleanField(default=True)
    nsn = models.ForeignKey(Nsn, null=True)
    images = models.ManyToManyField('PartImage')
    characteristics = models.ManyToManyField('Characteristic')

    def __unicode__(self):
        return self.number

    class Meta:
        unique_together = ('number', 'company',)

    def save(self, *args, **kwargs):
        self.number = self.number.strip().upper()
        self.description = self.description.strip().upper()
        super(Part, self).save(*args, **kwargs)
    
    @models.permalink
    def get_absolute_url(self):
        return ('parts.views.detail', (), {
            'part_id': str(self.id) + '/' + str(self.number),})

class Xref(models.Model):
    user = models.ForeignKey(User, null=True)
    part = models.ForeignKey('Part')
    xrefpart = models.ForeignKey('Part', related_name='xrefpart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)

    class Meta:
        unique_together = ('part', 'xrefpart',)

class Characteristic(models.Model):
    key = models.CharField(max_length=50, unique=True)
    values = models.ManyToManyField('CharacteristicValue')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, null=True)

    def save(self, *args, **kwargs):
        self.key = self.key.strip().upper()
        super(Characteristic, self).save(*args, **kwargs)

class CharacteristicValue(models.Model):
    value = models.CharField(max_length=128, unique=True)

    def save(self, *args, **kwargs):
        self.value = self.value.strip().upper()
        super(CharacteristicValue, self).save(*args, **kwargs)

class PartImage(models.Model):
    image = ImageField(upload_to='part_images')
    user = models.ForeignKey(User, null=False)
    approved = models.BooleanField(default=True)
    album_cover = models.BooleanField(default=False)

class PartModerator(CommentModerator):
    email_notification = True

moderator.register(Part, PartModerator)


