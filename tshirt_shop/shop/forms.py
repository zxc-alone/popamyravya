from django import forms
from .models import Product

class ProductSearchForm(forms.Form):
    """Форма поиска товаров"""
    query = forms.CharField(label='Поиск', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Поиск футболок...'}))
    size = forms.ChoiceField(label='Размер', required=False, choices=[('', 'Все')] + Product.SIZES, widget=forms.Select(attrs={'class': 'form-select'}))
    color = forms.ChoiceField(label='Цвет', required=False, choices=[('', 'Все')] + Product.COLORS, widget=forms.Select(attrs={'class': 'form-select'}))
    min_price = forms.DecimalField(label='Цена от', required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'От'}))
    max_price = forms.DecimalField(label='Цена до', required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'До'}))