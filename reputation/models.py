from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.conf import settings

from parts.models import Part, Attribute, PartImage

class ReputationProfile(models.Model):
    user = models.OneToOneField(User)
    reputation_sum = models.IntegerField()
    badges = models.ManyToManyField('Badge', related_name='rep_badges')
    

class ReputationAction(models.Model):
    user = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)
    point_value = models.IntegerField()
    action = models.CharField(max_length=12)
    
    def reputation_event(sender, instance, created, **kwargs):
        if sender is Part:
            points = settings.REP_VALUE_NEW_PART
            action = 'NEW_PART'
        elif sender is Attribute:
            points = settings.REP_VALUE_NEW_ATTRIBUTE
            action = 'NEW_ATTR'
        elif sender is PartImage:
            points = settings.REP_VALUE_NEW_IMAGE
            action = 'NEW_IMG'
        else:
            pass
        
        if created:
            ra = ReputationAction(user=instance.user, point_value=points, action=action)
            ra.save()
        else:
            pass
    
    post_save.connect(reputation_event, sender=Part)
    post_save.connect(reputation_event, sender=Attribute)
    post_save.connect(reputation_event, sender=PartImage)
    
class Badge(models.Model):
    name = models.CharField(max_length=32)
    required_points = models.IntegerField(null=True)
    required_action = models.CharField(max_length='64', null=True)
    points_earned = models.IntegerField()
