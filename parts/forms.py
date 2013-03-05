from django import forms
from parts.models import Part
from search.widgets import JQueryAutoComplete

class MetadataForm(forms.Form):
    key = forms.CharField(max_length=48)
    value = forms.CharField(max_length=128)

class BuyLinkForm(forms.Form):
   url = forms.URLField(required=True)
   price = forms.DecimalField(decimal_places=4, required=True)
   company = forms.CharField(max_length=48)
   

class XrefForm(forms.Form):
    part = forms.CharField(
        widget=JQueryAutoComplete(
            source='/search/autocomplete/?type=part',
            attrs={'max_length':48, 'placeholder':'New Part #'},
            options={"minLength":3}))

    company = forms.CharField(max_length=48)

    desc = forms.CharField(max_length=256, required=False)
    copy_attrs = forms.BooleanField(required=False)
    
class ImageUploadForm(forms.Form):
    file = forms.FileField(required=True)
