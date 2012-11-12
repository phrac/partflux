from django.db import models

class Nsn(models.Model):
    number = models.CharField(max_length=16, unique=True)
    fsc = models.ForeignKey('Fsc', null=True)
    description = models.TextField()
    niin = models.IntegerField(unique=True)
    codification_country = CharField(max_length=16, null=True)
    adp_code = CharField(max_length=16, null=True)
    dml_code = CharField(max_length=16, null=True)
    hmic = BooleanField(max_length=16, null=True)
    pmic = BooleanField(max_length=16, null=True)
    esdc = BooleanField(max_length=16, null=True)
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
        
class Mrc(models.Model):
    nsn = models.ForeignKey(Nsn)
    mrc = CharField(max_length=10)
    req = CharField(max_length=64)
    reply = CharField(max_length=256)
