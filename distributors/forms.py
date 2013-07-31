from django import forms
from distributors.models import Distributor, DistributorSKU

class DistributorSKUForm(forms.ModelForm):
    class Meta:
        model = DistributorSKU
        exclude = ['part', 'updated']
