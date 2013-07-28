from django import forms
from distributors.models import Distributor, DistributorSKU

class DistributorSKUForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        part = kwargs.pop('part')
        super(DistributorSKUForm, self).__init__(*args, **kwargs)
    class Meta:
        model = DistributorSKU
        exclude = ['part']
