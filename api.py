from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import DjangoAuthorization, Authorization
from tastypie import fields
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from parts.models import Part, Attribute
from companies.models import Company

from django.contrib.auth.models import User
from django.db import models
from tastypie.models import create_api_key

models.signals.post_save.connect(create_api_key, sender=User)

class AttributeResource(ModelResource):
    part = fields.ToOneField('partfindr.api.PartResource', 'part')
    class Meta:
        queryset = Attribute.objects.all()
        fields = ['key', 'value']
        resource_name = 'attribute'
        filtering = {'pk':['in','exact'],}
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()

class CompanyResource(ModelResource):
    class Meta:
        queryset = Company.objects.all()
        resource_name = 'company'
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        filtering = {'name': ['exact'],}

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()

class PartResource(ModelResource):
    attributes = fields.ToManyField('partfindr.api.AttributeResource',
                                    'attribute_set',
                                    related_name='part',
                                    full=True,
                                    null=True
                                    )
    company = fields.ToOneField('partfindr.api.CompanyResource',
                                'company',
                                related_name='company',
                                full=True
                               )
    user = fields.ToOneField('partfindr.api.UserResource',
                             'user',
                             related_name='user'
                            )

    class Meta:
        queryset = Part.objects.all()
        resource_name = 'part'

        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        filtering = {'pk':['in','exact'],}
