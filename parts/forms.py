from django import forms
from django.forms import ModelForm
from parts.models import Part, Metadata

class MetadataForm(ModelForm):
    class Meta:
        model = Metadata
        fields = ('key', 'value',)

class XrefForm(forms.Form):
    part = forms.CharField(max_length=48)
    company = forms.CharField(max_length=48)
    desc = forms.CharField(max_length=48, required=False)
