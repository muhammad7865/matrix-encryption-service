from django.contrib import admin
from .models import APIKey, ServiceUsage

@admin.register(APIKey)
class APIKeyAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'is_active', 'usage_count', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'user__username']

@admin.register(ServiceUsage)
class ServiceUsageAdmin(admin.ModelAdmin):
    list_display = ['user', 'operation_type', 'algorithm_used', 'processing_time', 'timestamp']
    list_filter = ['operation_type', 'algorithm_used', 'processing_method', 'timestamp']
    search_fields = ['user__username']
