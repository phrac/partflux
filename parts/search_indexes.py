from haystack import indexes
from partfindr.models import Part


class PartIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    description = indexes.CharField(model_attr='description')
    company = indexes.DateTimeField(model_attr='company')

    def get_model(self):
        return Part
