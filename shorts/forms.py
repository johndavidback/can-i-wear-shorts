__author__ = 'john'

from django import forms


class SearchForm(forms.Form):
    location = forms.CharField(max_length=200,
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control', 'placeholder': 'Cincinnati, OH'}
                               )
    )