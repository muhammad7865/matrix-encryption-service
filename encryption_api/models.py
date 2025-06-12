from django.db import models
from django.conf import settings

class EncryptionJob(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    ALGORITHM_CHOICES = [
        ('hill_cipher', 'Hill Cipher'),
        ('matrix_transform', 'Matrix Transformation'),
        ('advanced_matrix', 'Advanced Matrix Encryption'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    job_id = models.CharField(max_length=32, unique=True)
    algorithm = models.CharField(max_length=50, choices=ALGORITHM_CHOICES)
    processing_method = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    input_type = models.CharField(max_length=20)
    input_size = models.IntegerField()
    matrix_size = models.IntegerField(default=8)
    parallel_workers = models.IntegerField(default=1)
    processing_time = models.FloatField(null=True, blank=True)
    speedup_factor = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(blank=True)

class EncryptedFile(models.Model):
    job = models.ForeignKey(EncryptionJob, on_delete=models.CASCADE)
    original_filename = models.CharField(max_length=255)
    encrypted_file = models.FileField(upload_to='encrypted_files/')
    encryption_key_hash = models.CharField(max_length=64, default='')
    file_size = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
