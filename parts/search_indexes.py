from haystack import indexes
from parts.models import Part, Attribute
from django.utils.encoding import smart_str

class PartIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(boost=2, document=True, use_template=True)
    number = indexes.EdgeNgramField(model_attr='number', boost=1.5, indexed=True,
                                index_fieldname='number', stored=True)
    company = indexes.CharField(model_attr='company')
    created = indexes.DateTimeField(model_attr='created_at')
    url = indexes.CharField(indexed=False)
    
    def prepare_url(self, obj):
        return "http://partengine.org%s" % obj.get_absolute_url()
    
    def get_model(self):
        return Part

    def get_updated_field(self):
        return 'updated_at'
