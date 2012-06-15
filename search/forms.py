from django import forms
from widgets import JQueryAutoComplete


class SearchForm(forms.Form):
    q = forms.CharField(widget=JQueryAutoComplete(source='/search/ac/?type=part',
                                                        attrs={'max_length':48,}))
