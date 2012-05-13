from haystack import indexes
from nsn.models import Nsn

class NsnIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    fsc = indexes.CharField(model_attr='fsc')

    def get_model(self):
        return Nsn
