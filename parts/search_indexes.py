from haystack import indexes
from parts.models import Part, Attribute

class PartIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    number = indexes.NgramField(model_attr='number', boost=3)
    company = indexes.CharField(model_attr='company', faceted=True)
    attributes = indexes.MultiValueField(faceted=True)  
    
    def get_model(self):
        return Part

    def prepare_attributes(self, obj):
        return [str("%s: %s" % (a.key, a.value)) for a in obj.attribute_set.all()]

    def get_updated_field(self):
        return 'updated_at'