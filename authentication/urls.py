from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('api-keys/', views.manage_api_keys, name='api_keys'),
    path('profile/', views.profile, name='profile'),
]
