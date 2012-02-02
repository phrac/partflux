from django.db import models

class Nsn(models.Model):
    number = models.CharField(max_length=13, unique=True)
    fsc = models.ForeignKey('Fsc')
    description = models.TextField()
     
    def __unicode__(self):
        return self.number
    

class Fsc(models.Model):
    number = models.CharField(max_length=4, unique=True)
    description = models.TextField()

    def __unicode__(self):
        return self.number
