from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.conf import settings

from parts.models import Part, Attribute, PartImage
from reputation.models import ReputationAction

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    facebook_profile = models.URLField()
    twitter_profile = models.URLField()
    linkedin_profile = models.URLField()
    location = models.CharField(max_length=64)
    reputation = models.IntegerField(default=0)
    

    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    def can_vote(self):
        if self.reputation >= settings.MINIMUM_VOTE_REPUTATION:
            return True
        else:
            return False

    def update_total_rep(sender, instance, created, **kwargs):
        from django.db.models import Sum
        r = ReputationAction.objects.filter(user=instance.user).aggregate(total_rep=Sum('point_value'))
        self.reputation = r.get('total_rep')
        self.save()

    post_save.connect(create_user_profile, sender=User)
    post_save.connect(update_total_rep, sender=ReputationAction)


class UserFavoritePart(models.Model):
    user = models.ForeignKey(User)
    part = models.ForeignKey(Part)
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(null=True)

    class Meta:
        unique_together = ('user', 'part',)


