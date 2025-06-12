from django.shortcuts import render
from django.http import JsonResponse

def analytics_dashboard(request):
    return render(request, 'analytics/dashboard.html')

def get_metrics(request):
    return JsonResponse({'message': 'Analytics metrics endpoint'})

def get_performance_data(request):
    return JsonResponse({'message': 'Performance data endpoint'})
