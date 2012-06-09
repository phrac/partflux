from haystack import indexes
from parts.models import Part

class PartIndex(indexes.RealTimeSearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    number = indexes.NgramField(model_attr='number', boost=3)
    company = indexes.CharField(model_attr='company', faceted=True)
    attributes = indexes.FacetMultiValueField()
    #values = indexes.FacetMultiValueField()

    def prepare_attributes(self, obj):
        attrs = []
        for key, value in obj.attributes.iteritems():
            values = value.split("|")
            for v in values:
                attrs.append("_%s_%s" % (key, v))
        return attrs

    
    def prepare_value(self):
        pass
        
    def get_model(self):
        return Part

    def get_updated_field(self):
        return 'updated_at'


