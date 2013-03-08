from django import forms
from django.forms import ModelForm
from partgroups.models import PartGroup


class PartGroupForm(ModelForm):
    name = forms.CharField(max_length=32)
    description = forms.CharField(required=True, widget=forms.Textarea)
    private = forms.BooleanField(required=False)
    
    class Meta:
        model = PartGroup
        
class PartGroupAddForm(forms.Form):
    name = forms.CharField(max_length=32)
    description = forms.CharField(required=True, widget=forms.Textarea)
    private = forms.BooleanField(required=False)



