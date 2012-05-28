from mongoengine import *

class Company(Document):
    name = StringField(max_length=128, unique=True)
    description = StringField()
    url = URLField()
    email = EmailField(max_length=32)
    phone = StringField(max_length=16)
    fax = StringField(max_length=16)
    city = StringField(max_length=32)
    state = StringField(max_length=32)
    country = StringField(max_length=32)
    created_at = DateTimeField()
    updated_at = DateTimeField()

    def save(self, *args, **kwargs):
        self.name = self.name.strip().upper()
        super(Company, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return ('companies.views.details', [str(self.id)])
