from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User)

    reputation = models.IntegerField()
    facebook_profile = models.URLField()
    twitter_profile = models.URLField()
    linkedin_profile = models.URLField()


