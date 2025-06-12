from django.contrib.auth.models import AbstractUser
from django.db import models
import secrets
import string

class User(AbstractUser):
    email = models.EmailField(unique=True)
    company = models.CharField(max_length=200, blank=True)
    api_usage_limit = models.IntegerField(default=1000)
    is_premium = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Add these related_name arguments to fix the clash
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

class APIKey(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='api_keys')
    name = models.CharField(max_length=100)
    key = models.CharField(max_length=64, unique=True)
    is_active = models.BooleanField(default=True)
    usage_count = models.IntegerField(default=0)
    last_used = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_api_key()
        super().save(*args, **kwargs)

    def generate_api_key(self):
        alphabet = string.ascii_letters + string.digits
        return 'eaas_' + ''.join(secrets.choice(alphabet) for _ in range(32))

    def __str__(self):
        return f"{self.user.username} - {self.name}"

class ServiceUsage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    api_key = models.ForeignKey(APIKey, on_delete=models.CASCADE, null=True, blank=True)
    operation_type = models.CharField(max_length=50)
    algorithm_used = models.CharField(max_length=50)
    processing_method = models.CharField(max_length=20)
    data_size = models.IntegerField()
    processing_time = models.FloatField()
    cpu_cores_used = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField(default=True)
    error_message = models.TextField(blank=True)
