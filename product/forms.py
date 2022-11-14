from django import forms


class ProductSearchForm(forms.Form):
    search = forms.CharField()
