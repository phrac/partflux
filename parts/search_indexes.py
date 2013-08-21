from haystack import indexes
from parts.models import Part, Attribute, Category
from distributors.models import DistributorSKU
from django.utils.encoding import smart_str

class PartIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    created = indexes.DateTimeField(model_attr='created_at')
    brand = indexes.CharField(model_attr='company', faceted=True, indexed=False)
    category = indexes.CharField(faceted=True, indexed=False)
    with_distributors = indexes.FacetBooleanField()
    with_image = indexes.FacetBooleanField()
    url = indexes.CharField(indexed=False)

    def prepare_with_image(self, obj):
        if obj.image_url:
            return True
        else:
            return False
    
    def prepare_with_distributors(self, obj):
        if DistributorSKU.objects.filter(part=obj).count() > 0:
            return True
        else:
            return False
    
    def prepare_category(self, obj):
        for c in obj.categories.all():
            return c.name

    def prepare_url(self, obj):
        return "http://partflux.com%s" % obj.get_absolute_url()
        
    def get_model(self):
        return Part

    def get_updated_field(self):
        return 'updated_at'
        
class CategoryIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    
    def get_model(self):
        return Category
        
