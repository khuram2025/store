from django.shortcuts import render

from products.models import Category, Product

def home(request):
    main_categories = Category.objects.filter(parent__isnull=True, is_active=True)
    products = Product.objects.filter(is_active=True)
    return render(request, 'suha/home.html', {'main_categories': main_categories, 'products':products})
