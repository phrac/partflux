from django.db import models
from django_orm.postgresql.fts.fields import VectorField
from django_orm.manager import FtsManager as SearchManager
from django.contrib.auth.models import User
from django_orm.postgresql import hstore

from companies.models import Company
from partfindr.custom_fields import ListField

class Part(models.Model):
    number = models.CharField(max_length=48)
    description = models.TextField()
    company = models.ForeignKey(Company)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, null=True)
    hits = models.IntegerField(default=0, editable=False)
    approved = models.BooleanField(default=True)
    tsv = VectorField()
    metadata = hstore.DictionaryField(db_index=True) 
    objects = SearchManager(
        search_field = 'tsv',
        fields = 'description',
    )
    
    def __unicode__(self):
        return self.number
    
    class Meta:
        unique_together = ('number', 'company',)

    def save(self, *args, **kwargs):
        self.number = self.number.strip().upper()
        self.description = self.description.strip().upper()
        super(Part, self).save(*args, **kwargs)

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

class PartComment(models.Model):
    part = models.ForeignKey('Part')
    user = models.ForeignKey(User, null=True)
    parent_comment = models.ForeignKey('PartComment')
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_edit = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return self.comment


