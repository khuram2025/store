from django import forms
from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .models import (
    Category,
    Product,
    ProductImage,
    ProductSpecification,
    ProductSpecificationValue,
 
)

admin.site.register(Category, MPTTModelAdmin)


class ProductSpecificationInline(admin.TabularInline):
    model = Category.specifications.through 


  

class ProductImageInline(admin.TabularInline):
    model = ProductImage


class ProductSpecificationValueInline(admin.TabularInline):
    model = ProductSpecificationValue


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProductSpecificationValueInline,
        ProductImageInline,
    ]
from .models import (
    ProductChoice,
)

class ProductChoiceInline(admin.TabularInline):
    model = ProductChoice

class ProductSpecificationAdmin(admin.ModelAdmin):
    inlines = [
        ProductChoiceInline,
    ]

admin.site.register(ProductSpecification, ProductSpecificationAdmin)

class CategoryAdmin(MPTTModelAdmin):
    inlines = [
        ProductSpecificationInline,
    ]

admin.site.unregister(Category)
admin.site.register(Category, CategoryAdmin)
