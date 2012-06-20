from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.conf import settings


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    reputation = models.IntegerField()
    facebook_profile = models.URLField()
    twitter_profile = models.URLField()
    linkedin_profile = models.URLField()
    apikey = models.CharField(max_length=128)
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




