from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from parts.models import Part, Attribute, PartImage, BuyLink, Xref

class ReputationAction(models.Model):
    user = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)
    point_value = models.IntegerField()
    action = models.CharField(max_length=12)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    
    def get_human_action(self):
        if self.action == 'NEW_PART':
            action = 'Created a new part'
        elif self.action == 'NEW_ATTR':
            action = 'Added an attribute'
        elif self.action == 'NEW_IMG':
            action = 'Uploaded a new image'
        elif self.action == 'NEW_BUYLINK':
            action = 'Added a new purchase link'
        elif self.action == 'NEW_XREF':
            action = 'Added a cross reference'
        else:
            action = 'Unknown action'
        return action

    def get_object_url(self):
        print self.content_type.name
        if self.content_object is not None and self.object_id is not None:
            if self.content_type.name == 'attribute':
                return self.content_object.part.get_absolute_url()
            elif self.content_type.name == 'part image':
                part = Part.objects.filter(images__id=self.object_id)
                return part[0].get_absolute_url()
            elif self.content_type.name == 'part':
                return self.content_object.get_absolute_url()
            elif self.content_type.name == 'buy link':
                return self.content_object.part.get_absolute_url()
            elif self.content_type.name == 'xref':
                return self.content_object.part.get_absolute_url()

    def get_object_name(self):
        if self.content_object is not None and self.object_id is not None:
            if self.content_type.name == 'attribute':
                return self.content_object.part.number
            elif self.content_type.name == 'part image':
                part = Part.objects.filter(images__id=self.object_id)
                return part[0].number
            elif self.content_type.name == 'part':
                return self.content_object.number
            elif self.content_type.name == 'buy link':
                return self.content_object.part.number
            elif self.content_type.name == 'xref':
                return self.content_object.part.number

    
    def reputation_event(sender, instance, created, **kwargs):
        if instance.user.id == 2:
            pass
        else:
            if sender is Part:
                points = settings.REP_VALUE_NEW_PART
                action = 'NEW_PART'
            elif sender is Attribute:
                points = settings.REP_VALUE_NEW_ATTRIBUTE
                action = 'NEW_ATTR'
            elif sender is PartImage:
                points = settings.REP_VALUE_NEW_IMAGE
                action = 'NEW_IMG'
            elif sender is BuyLink:
                points = settings.REP_VALUE_NEW_BUYLINK
                action = 'NEW_BUYLINK'
            elif sender is Xref:
                points = settings.REP_VALUE_NEW_XREF
                action = 'NEW_XREF'
            else:
                pass
            
            if created and instance.user is not None:
                ra = ReputationAction(content_object=instance, user=instance.user, point_value=points, action=action)
                ra.save()
            else:
                pass
    
    post_save.connect(reputation_event, sender=Part)
    post_save.connect(reputation_event, sender=Attribute)
    post_save.connect(reputation_event, sender=PartImage)
    post_save.connect(reputation_event, sender=BuyLink)
    post_save.connect(reputation_event, sender=Xref)
    
class Badge(models.Model):
    name = models.CharField(max_length=32)
    required_points = models.IntegerField(null=True)
    required_action = models.CharField(max_length='64', null=True)
    points_earned = models.IntegerField()
