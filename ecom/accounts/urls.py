from django.urls import path
from .views import register
from . import views
from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),

    path('profile/<int:pk>/', views.profile_detail_view, name='profile-detail'),
    path('profile/<int:pk>/edit', views.edit_profile, name='edit_profile'),

    # Other paths...
]
