from django import forms
from companies.models import Company

class CompanyAdminForm(forms.Form):
    name = forms.CharField(max_length=128)
    description = forms.CharField(widget=forms.widgets.Textarea(),
                                  required=False)
    url = forms.URLField(required=False)
    wikipedia_url = forms.URLField(required=False)
    facebook_url = forms.URLField(required=False)
    twitter_url = forms.URLField(required=False)
    linkedin_url = forms.URLField(required=False)
    is_public = forms.BooleanField(required=False)
    email = forms.EmailField(max_length=32, required=False)
    phone = forms.CharField(max_length=16, required=False)
    fax = forms.CharField(max_length=16, required=False)
    address1 = forms.CharField(max_length=64, required=False)
    address2 = forms.CharField(max_length=64, required=False)
    city = forms.CharField(max_length=32, required=False)
    state = forms.CharField(max_length=32, required=False)
    country = forms.CharField(max_length=32, required=False)
    zipcode = forms.CharField(max_length=8, required=False)
    logo = forms.ImageField(required=False)

