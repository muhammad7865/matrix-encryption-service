from django.db import models
from django.conf import settings

class SystemMetrics(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    cpu_usage = models.FloatField()
    memory_usage = models.FloatField()
    active_jobs = models.IntegerField()
    total_requests = models.IntegerField()
    average_response_time = models.FloatField()

class AlgorithmPerformance(models.Model):
    algorithm = models.CharField(max_length=50)
    matrix_size = models.IntegerField()
    avg_serial_time = models.FloatField()
    avg_parallel_time = models.FloatField()
    max_speedup = models.FloatField()
    optimal_workers = models.IntegerField()
    last_updated = models.DateTimeField(auto_now=True)
