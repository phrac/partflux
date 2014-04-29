from django import forms
from django_select2 import *
from parts.models import Part, Category
from companies.models import Company

class CategoryChoice(AutoModelSelect2Field):
    queryset = Category.objects
    search_fields = ['name__icontains',]

class CompanyChoice(AutoModelSelect2Field):
    queryset = Company.objects
    search_fields = ['name__istartswith',]
    
class PartChoice(AutoModelSelect2Field):
    queryset = Part.objects
    search_fields = ['number__istartswith', ]

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
    part = PartChoice()

    desc = forms.CharField(max_length=256, required=False)
    copy_attrs = forms.BooleanField(required=False)
    
class ImageUploadForm(forms.Form):
    file = forms.FileField(required=True)

class NewPartForm(forms.ModelForm):
    class Meta:
        model = Part
        fields = ('number', 'category', 'description', 'company',)

    category = CategoryChoice()
    company = CompanyChoice()
        
