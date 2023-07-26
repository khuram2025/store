from django.urls import path
from .views import register
from . import views
from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', views.login_view, name='login'),
    path('accounts/', views.accounts, name='accounts'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),

    path('profile/<int:pk>/', views.profile_detail_view, name='profile-detail'),
    path('profile/<int:pk>/edit', views.edit_profile, name='edit_profile'),

 
    path('reset_password_request/', views.reset_password_request_view, name='password_reset_request'),
    path('verify_otp/<int:user_id>/', views.verify_otp_view, name='verify_otp'),
    path('reset_password/<int:user_id>/', views.reset_password_view, name='reset_password'),


    #... (your other urls)




    # Other paths...
]
