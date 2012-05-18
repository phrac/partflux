from django.db import models
from django.contrib.auth.models import User

from parts.models import Part

class PartGroup(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User)
    private = models.NullBooleanField(default=False, null=True)
    parent_group = models.ForeignKey('PartGroup', null=True)
    parts = models.ManyToManyField(Part)
    
    class Meta:
        unique_together = ('name', 'user',)
    
    def __unicode__(self):
        return self.name

