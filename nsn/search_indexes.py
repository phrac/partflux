from haystack import indexes
from nsn.models import Nsn

class NsnIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    created = indexes.DateTimeField(model_attr='updated_at')
    url = indexes.CharField(indexed=False)
    
    def prepare_url(self, obj):
        return "http://partengine.org%s" % obj.get_absolute_url()

    def get_model(self):
        return Nsn

    def get_updated_field(self):
        return 'updated_at'
