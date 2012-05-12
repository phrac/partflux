from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(null=True)
    url = models.URLField(null=True)
    email = models.EmailField(null=True)
    phone = models.CharField(null=True)
    fax = models.CharField(null=True)
    city = models.CharField(max_length=32, null=True)
    state = models.CharField(max_length=32, null=True)
    country = models.CharField(max_length=32, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.name = self.name.strip().upper()
        super(Company, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name
