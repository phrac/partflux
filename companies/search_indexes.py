from haystack import indexes
from companies.models import Company

class CompanyIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.EdgeNgramField(model_attr='name')
    created = indexes.DateTimeField(model_attr='created_at')
    url = indexes.CharField(indexed=False)
    
    def prepare_url(self, obj):
        return "http://partengine.org%s" % obj.get_absolute_url()
    
    def get_model(self):
        return Company

    def get_updated_field(self):
        return 'updated_at'
