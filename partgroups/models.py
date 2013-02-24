from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

from parts.models import Part

class PartGroup(models.Model):
    name = models.CharField(max_length=128)
    slug = models.CharField(max_length=64, null=True)
    description = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User)
    private = models.NullBooleanField(default=False, null=True)
    parent_group = models.ForeignKey('PartGroup', null=True)
    parts = models.ManyToManyField('PartGroupItem')
    
    class Meta:
        unique_together = ('name', 'user',)
    
    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(PartGroup, self).save(*args, **kwargs)
    
    @models.permalink
    def get_absolute_url(self):
        return ('partgroups.views.detail', [self.id, str(self.slug)])

class PartGroupItem(models.Model):
    part = models.ForeignKey(Part)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    required = models.BooleanField(default=True)
