from django.db import models
from django.contrib.auth.models import User
from django_orm.postgresql import hstore

from parts.models import Part

class PartGroup(models.Model):
    name = models.CharField(max_length=48)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, null=True)
    private = models.BooleanField(default=False)
    objects = hstore.HStoreManager()
    
    def __unicode__(self):
        return self.name
    

