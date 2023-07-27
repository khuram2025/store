from django import forms
from .models import Category

class CategoryForm(forms.ModelForm):
    parent = forms.ModelChoiceField(
        queryset=Category.objects.all(), 
        required=False,  # make parent field optional
    )

    class Meta:
        model = Category
        fields = ('name', 'slug', 'parent', 'is_active', 'image',)

from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('product_type', 'category', 'title', 'description', 'slug', 'regular_price', 'discount_price', 'is_active')