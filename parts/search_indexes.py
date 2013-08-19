from haystack import indexes
from parts.models import Part, Attribute, Category
from django.utils.encoding import smart_str

class PartIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    created = indexes.DateTimeField(model_attr='created_at')
    
    def get_model(self):
        return Part

    def get_updated_field(self):
        return 'updated_at'
        
class CategoryIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    
    def get_model(self):
        return Category
        
