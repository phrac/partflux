from django import forms
from django_select2 import *
from parts.models import Part, Category

class CategoryChoice(AutoModelSelect2Field):
    queryset = Category.objects
    search_fields = ['name__icontains',]

class MetadataForm(forms.Form):
    key = forms.CharField(max_length=48)
    value = forms.CharField(max_length=128)

class BuyLinkForm(forms.Form):
   url = forms.URLField(required=True)
   price = forms.DecimalField(decimal_places=4, required=True)
   company = forms.CharField(max_length=48)
   
class ASINForm(forms.Form):
   asin = forms.CharField(max_length=10)
   
class XrefForm(forms.Form):
    part = forms.CharField(max_length=48)
    company = forms.CharField(max_length=48)

    desc = forms.CharField(max_length=256, required=False)
    copy_attrs = forms.BooleanField(required=False)
    update_all_xrefs = forms.BooleanField(required=False)
    
class ImageUploadForm(forms.Form):
    file = forms.FileField(required=True)

class NewPartForm(forms.ModelForm):
    class Meta:
        model = Part
        fields = ('number', 'category', 'description', 'company',)

    category = CategoryChoice()
        
