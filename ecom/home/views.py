from django.shortcuts import render
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from products.models import Category, Product

def home(request):
    main_categories = Category.objects.filter(parent__isnull=True, is_active=True)
    most_viewed_products = Product.objects.filter(is_active=True).order_by('-views')[:6]
    products = Product.objects.filter(is_active=True)
    now = timezone.now()

    


    return render(request, 'suha/home.html', {
        'main_categories': main_categories,
        'products':products,
        'most_viewed_products': most_viewed_products,
   

                                               })
