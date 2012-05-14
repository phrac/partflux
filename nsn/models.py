from django.db import models

class Nsn(models.Model):
    number = models.CharField(max_length=16, unique=True)
    fsc = models.ForeignKey('Fsc', null=True)
    description = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
     
    def __unicode__(self):
        return self.number
    

class Fsc(models.Model):
    number = models.CharField(max_length=4, unique=True)
    description = models.TextField()

    def __unicode__(self):
        return self.number
