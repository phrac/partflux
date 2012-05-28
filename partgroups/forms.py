from django import forms
from parts.models import Part

class PartGroupForm(forms.Form):
    name = forms.CharField(max_length=32)
    description = forms.CharField(max_length=128, required=True)
    private = forms.BooleanField(required=False)



