from haystack import indexes
from companies.models import Company

class CompanyIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.EdgeNgramField(model_attr='name')  
    
    def get_model(self):
        return Company

    def get_updated_field(self):
        return 'updated_at'
