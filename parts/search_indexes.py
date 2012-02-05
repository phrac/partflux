from haystack.indexes import *
from haystack import site
from parts.models import Part


class PartIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    description = CharField(model_attr='description')
    company = DateTimeField(model_attr='company')

site.register(Part, PartIndex)
