from django import forms
from parts.models import Part

class PartGroupForm(forms.Form):
    name = forms.CharField(max_length=48)
    description = forms.CharField(max_length=128, required=False)
    private = forms.BooleanField(required=True)



