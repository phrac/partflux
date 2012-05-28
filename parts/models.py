from django.db import models
from mongoengine import *
from django.contrib.auth.models import User
from sorl.thumbnail import ImageField

from companies.models import Company

class Part(DynamicDocument):
    number = StringField(max_length=48, unique_with='company')
    description = StringField()
    company = ReferenceField('Company')
    created_at = DateTimeField()
    updated_at = DateTimeField()
    user = ReferenceField('User')
    hits = IntField(default=0)
    approved = BooleanField(default=True)
    xrefs = ListField(EmbeddedDocumentField('Xref'))
    characteristics = ListField(EmbeddedDocumentField('Characteristic'))

    def save(self, *args, **kwargs):
        self.number = self.number.strip().upper()
        super(Part, self).save(*args, **kwargs)
    
    def get_absolute_url(self):
        return ('parts.views.detail', (), {
            'part_id': str(self.id) + '/' + str(self.number),})

class Xref(EmbeddedDocument):
    user = ReferenceField('User')
    part = ReferenceField('Part')
    created_at = DateTimeField()
    updated_at = DateTimeField()
    upvotes = IntField(default=0)
    downvotes = IntField(default=0)

class Characteristic(EmbeddedDocument):
    key = StringField()
    value = ListField(StringField())
    user = ReferenceField('User')
    created_at = DateTimeField()
    updated_at = DateTimeField()
    upvotes = IntField(default=0)
    downvotes = IntField(default=0)

