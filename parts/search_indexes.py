from haystack import indexes
from parts.models import Part


class PartIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    number = indexes.NgramField(model_attr='number', boost=3)
    company = indexes.CharField(model_attr='company', faceted=True)
    lastupdate = indexes.DateTimeField(model_attr='updated_at')

    def get_model(self):
        return Part

