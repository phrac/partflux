from django.db import models
from django.contrib.auth.models import User

from parts.models import Part

class PartGroup(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, null=True)
    private = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.name

class PartGroupItem(models.Model):
    partgroup = models.ForeignKey('PartGroup')
    part = models.ForeignKey(Part)

