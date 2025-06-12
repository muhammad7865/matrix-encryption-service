from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.analytics_dashboard, name='analytics_dashboard'),
    path('api/metrics/', views.get_metrics, name='get_metrics'),
    path('api/performance/', views.get_performance_data, name='get_performance_data'),
]
