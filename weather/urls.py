from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('autocomplete/', views.city_autocomplete, name='city_autocomplete'),
    path('login/', auth_views.LoginView.as_view(template_name='weather/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]