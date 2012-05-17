from django.db import models
from django.contrib.auth.models import User
from django.contrib.comments.moderation import CommentModerator, moderator
from django_orm.postgresql import hstore
from sorl.thumbnail import ImageField

from companies.models import Company
from nsn.models import Nsn

class Part(models.Model):
    number = models.CharField(max_length=48)
    description = models.TextField()
    company = models.ForeignKey(Company)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, null=True)
    hits = models.IntegerField(default=0, editable=False)
    approved = models.BooleanField(default=True)
    metadata = hstore.DictionaryField(db_index=True) 
    nsn = models.ForeignKey(Nsn, null=True)

    objects = hstore.HStoreManager()

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

class PartImage(models.Model):
    part = models.ForeignKey('Part')
    image = ImageField(upload_to='part_images')
    user = models.ForeignKey(User, null=False)
    approved = models.BooleanField(default=True)

class PartModerator(CommentModerator):
    email_notification = True

moderator.register(Part, PartModerator)


