from django.db import models
from mongoengine import *
from django.contrib.auth.models import User

from parts.models import Part

class PartGroup(Document):
    name = StringField(max_length=128)
    description = StringField()
    created_at = DateTimeField()
    updated_at = DateTimeField()
    user = ReferenceField('User')
    private = BooleanField(default=False)
    parent_group = ReferenceField('PartGroup')
    
    class Meta:
        unique_together = ('name', 'user',)
    
    def __unicode__(self):
        return self.name
    
    @models.permalink
    def get_absolute_url(self):
        return ('partgroups.views.detail', None, { 'partgroup_id': str(self.id) })
