from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('api/encrypt/text/', views.encrypt_text, name='encrypt_text'),
    path('api/decrypt/text/', views.decrypt_text, name='decrypt_text'),
    path('api/benchmark/', views.benchmark_performance, name='benchmark'),
    path('api/job/<str:job_id>/', views.get_job_status, name='job_status'),
]
