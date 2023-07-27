from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [

    path('admin_categories/', views.admin_category_list, name='admin_category_list'),
    path('category/new/', views.category_new, name='category_new'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('category/<slug:slug>/edit/', views.category_edit, name='category_edit'),
    path('category/<slug:slug>/delete/', views.category_delete, name='category_delete'),

    path('categories/', views.category_list, name='category_list'),


    path('admin_products/', views.admin_product_list, name='admin_product_list'),
    path('<int:pk>/edit/', views.product_edit, name='product_edit'),
    path('<int:pk>/delete/', views.product_delete, name='product_delete'), 

    path('category/<int:category_id>/products/', views.products_by_category, name='products_by_category'),
    
]
