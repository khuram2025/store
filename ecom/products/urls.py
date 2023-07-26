from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    
    path('categories/', views.category_list, name='category_list'),
    path('category/new/', views.category_new, name='category_new'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('category/<slug:slug>/edit/', views.category_edit, name='category_edit'),
    path('category/<slug:slug>/delete/', views.category_delete, name='category_delete'),
   
    
]
