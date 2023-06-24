from django.urls import path
from .views import category_list

app_name = 'products'

urlpatterns = [
    # ... other paths here ...
    path('categories/', category_list, name='category_list'),
]
