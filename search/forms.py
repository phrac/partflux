from django import forms

class SearchForm(forms.form):
    q = forms.CharField(max_length=128, required=False)
