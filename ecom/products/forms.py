from django import forms
from .models import Category, Product, ProductSpecificationValue, ProductSpecification, ProductChoice, ProductImage

class CategoryForm(forms.ModelForm):
    parent = forms.ModelChoiceField(
        queryset=Category.objects.all(), 
        required=False,  # make parent field optional
    )

    class Meta:
        model = Category
        fields = ('name', 'slug', 'parent', 'is_active', 'image',)

from .models import Product


class CategorySelectForm(forms.Form):
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    
class ProductForm(forms.ModelForm):
    product_images = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)
    class Meta:
        model = Product
        fields = ['title', 'description', 'regular_price', 'discount_price', 'is_active', 'youtube_link', 'facebook_link', 'web_link',]
        exclude = ['product_image', 'seller_name', 'seller_mobile', 'seller_city']  # Add this line

    def __init__(self, *args, **kwargs):
        self.category = kwargs.pop('category', None)  # Store the category in the instance variable
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user and user.is_authenticated:
            if 'seller_name' in self.fields:
                self.fields['seller_name'].initial = user.name
            if 'seller_mobile' in self.fields:
                self.fields['seller_mobile'].initial = user.mobile_number
            if 'seller_city' in self.fields:
                self.fields['seller_city'].initial = user.userprofile.city

        if self.category:
            specs = self.category.specifications.all()
            for spec in specs:
                if spec.type == 'text':
                    self.fields[spec.name] = forms.CharField(label=spec.name)
                elif spec.type == 'choices':
                    choices = ProductChoice.objects.filter(specification=spec)
                    choice_list = [(choice.id, choice.value) for choice in choices]
                    self.fields[spec.name] = forms.ChoiceField(choices=choice_list)  
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.category = self.category
        if commit:
            instance.save()
            # Handle dynamic specifications
            for spec in self.category.specifications.all():
                spec_value = self.cleaned_data.get(spec.name)
                if spec_value:
                    if spec.type == 'text':
                        ProductSpecificationValue.objects.create(product=instance, specification=spec, text_value=spec_value)
                    elif spec.type == 'choices':
                        ProductSpecificationValue.objects.create(product=instance, specification=spec, choice_value_id=spec_value)
        return instance
    

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image']

ProductImageFormSet = forms.inlineformset_factory(Product, ProductImage, form=ProductImageForm, extra=1, max_num=15)
