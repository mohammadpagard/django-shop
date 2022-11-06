from django import forms


class ProductSearchForm(forms.Form):
    search = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
