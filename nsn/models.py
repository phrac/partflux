from django.db import models

class Nsn(models.Model):
    number = models.CharField(max_length=16, unique=True)
    fsc = models.ForeignKey('Fsc', null=True)
    description = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
     
    def __unicode__(self):
        return self.number
        
    def save(self, *args, **kwargs):
        self.number = self.number.strip().upper()
        self.description = self.description.strip().upper()
        super(Nsn, self).save(*args, **kwargs)
        
    @models.permalink
    def get_absolute_url(self):
        return ('nsn.views.detail', [self.id, str(self.number)])
    

class Fsc(models.Model):
    number = models.CharField(max_length=4, unique=True)
    description = models.TextField()

    def __unicode__(self):
        return self.number
