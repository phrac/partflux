from haystack import indexes
from parts.models import Part

class PartIndex(indexes.RealTimeSearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    number = indexes.NgramField(model_attr='number', boost=3)
    company = indexes.CharField(model_attr='company', faceted=True)

    def get_model(self):
        return Part

    def get_updated_field(self):
        return 'updated_at'


