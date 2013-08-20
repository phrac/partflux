from haystack import indexes
from parts.models import Part, Attribute, Category
from django.utils.encoding import smart_str

class PartIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    created = indexes.DateTimeField(model_attr='created_at')
    brand = indexes.CharField()
    url = indexes.CharField(indexed=False)
    
    def prepare_brand(self, obj):
        return obj.company.name
        
    def prepare_url(self, obj):
        return "http://partflux.com%s" % obj.get_absolute_url()
        
    def get_model(self):
        return Part

    def get_updated_field(self):
        return 'updated_at'
        
class CategoryIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    
    def get_model(self):
        return Category
        
