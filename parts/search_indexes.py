from haystack import indexes
from parts.models import Part, Attribute
from django.utils.encoding import smart_str

class PartIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    number = indexes.EdgeNgramField(model_attr='number', boost=3, indexed=True,
                                index_fieldname='number', stored=True)
    company = indexes.CharField(model_attr='company')  
    
    def get_model(self):
        return Part

    def get_updated_field(self):
        return 'updated_at'
