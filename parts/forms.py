from django import forms
from parts.models import Part, Metadata

class MetadataForm(forms.Form):
    key = forms.CharField(max_length=48)
    value = forms.CharField(max_length=96)

class XrefForm(forms.Form):
    part = forms.CharField(max_length=48)
    company = forms.CharField(max_length=48)
    desc = forms.CharField(max_length=48, required=False)

class SearchForm(forms.Form):
    q = forms.CharField(max_length=128)
