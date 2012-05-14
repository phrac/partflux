from haystack import indexes
from nsn.models import Nsn

class NsnIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    fsc = indexes.CharField(model_attr='fsc')
    lastupdate = indexes.DateTimeField(model_attr='updated_at')

    def get_model(self):
        return Nsn
