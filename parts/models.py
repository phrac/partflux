from django.db import models
from django_orm.postgresql import hstore
from django_orm.postgresql.fts.fields import VectorField
from django_orm.manager import FtsManager as SearchManager


class Part(models.Model):
    number = models.CharField(max_length=48)
    description = models.TextField()
    company = models.CharField(max_length=48)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    hits = models.IntegerField(default=0, editable=False)
    approved = models.BooleanField(default=True)
    tsv = VectorField()
    
    objects = SearchManager(
        search_field = 'tsv',
        fields = 'description',
    )
    
    def __unicode__(self):
        return self.number
    
    class Meta:
        unique_together = ('number', 'company',)

class Metadata(models.Model):
    part = models.ForeignKey('Part')
    key = models.CharField(max_length=48)
    value = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)

class Xref(models.Model):
    part = models.ForeignKey('Part')
    xrefpart = models.ForeignKey('Part', related_name='xrefpart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)

    class Meta:
        unique_together = ('part', 'xrefpart',)


class Comments(models.Model):
    part = models.ForeignKey('Part')

