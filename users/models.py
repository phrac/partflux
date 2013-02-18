from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.conf import settings

from parts.models import Part, Attribute, PartImage


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    reputation = models.IntegerField(default=0)
    facebook_profile = models.URLField()
    twitter_profile = models.URLField()
    linkedin_profile = models.URLField()
    location = models.CharField(max_length=64)
    

    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    post_save.connect(create_user_profile, sender=User)

    def can_vote(self):
        if self.reputation >= settings.MINIMUM_VOTE_REPUTATION:
            return True
        else:
            return False

    def increment_reputation(self, rep_points):
        self.reputation += rep_points
        self.save()
        
    def rep_signal(sender, instance, created, **kwargs):
        if sender is Part:
            inc = settings.REP_VALUE_NEW_PART
        elif sender is Attribute:
            inc = settings.REP_VALUE_NEW_ATTRIBUTE
        elif sender is PartImage:
            inc = settings.REP_VALUE_NEW_IMAGE
        else:
            pass
        
        if created:
            profile = UserProfile.objects.get(user=instance.user)
            profile.increment_reputation(inc)
        else:
            pass
        
    post_save.connect(rep_signal, sender=Part)
    post_save.connect(rep_signal, sender=Attribute)
    post_save.connect(rep_signal, sender=PartImage)        


class UserFavoritePart(models.Model):
    user = models.ForeignKey(User)
    part = models.ForeignKey(Part)
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(null=True)

    class Meta:
        unique_together = ('user', 'part',)


