from haystack import indexes
from nsn.models import Nsn

class NsnIndex(indexes.RealTimeSearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    
    def get_model(self):
        return Nsn

    def get_updated_field(self):
        return 'updated_at'
