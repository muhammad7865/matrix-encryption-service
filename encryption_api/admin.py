from django.contrib import admin
from .models import EncryptionJob, EncryptedFile

@admin.register(EncryptionJob)
class EncryptionJobAdmin(admin.ModelAdmin):
    list_display = ['job_id', 'user', 'algorithm', 'status', 'processing_method', 'created_at']
    list_filter = ['status', 'algorithm', 'processing_method', 'created_at']
    search_fields = ['job_id', 'user__username']

@admin.register(EncryptedFile)
class EncryptedFileAdmin(admin.ModelAdmin):
    list_display = ['original_filename', 'job', 'file_size', 'created_at']
    list_filter = ['created_at']
    search_fields = ['original_filename', 'job__job_id']
