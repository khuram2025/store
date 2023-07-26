from django.shortcuts import render

from products.models import Category, Product

def home(request):
    categories = Category.objects.all()
    products = Product.objects.filter(is_active=True)
    return render(request, 'pwa/home/index.html', {'categories': categories, 'products':products})
