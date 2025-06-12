from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.core.files.storage import default_storage
from django.conf import settings
import json
import uuid
import os
import time
import multiprocessing as mp
from .algorithms import MatrixEncryptionService
from .models import EncryptionJob, EncryptedFile
from authentication.models import ServiceUsage
import numpy as np
import base64

def dashboard(request):
    """Main dashboard view"""
    return render(request, 'dashboard.html')

@api_view(['POST'])
@permission_classes([AllowAny])  # Simplified for initial setup
def encrypt_text(request):
    """API endpoint for text encryption"""
    try:
        data = request.data
        text = data.get('text', '')
        algorithm = data.get('algorithm', 'hill_cipher')
        processing_method = data.get('processing_method', 'parallel')
        num_workers = data.get('num_workers', mp.cpu_count())
        matrix_size = data.get('matrix_size', 8)
        
        if not text:
            return Response({'error': 'No text provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create encryption job
        job = EncryptionJob.objects.create(
            user=request.user if request.user.is_authenticated else None,
            job_id=str(uuid.uuid4())[:8],
            algorithm=algorithm,
            processing_method=processing_method,
            input_type='text',
            input_size=len(text.encode()),
            matrix_size=matrix_size,
            parallel_workers=num_workers,
            status='processing'
        )
        
        # Initialize encryption service
        encryption_service = MatrixEncryptionService(algorithm=algorithm, matrix_size=matrix_size)
        
        start_time = time.time()
        
        if processing_method == 'serial':
            encrypted_matrix, processing_time = encryption_service.encrypt_serial(text)
        else:
            encrypted_matrix, processing_time = encryption_service.encrypt_parallel(text, num_workers=num_workers)
        
        total_time = time.time() - start_time
        
        # Update job status
        job.status = 'completed'
        job.processing_time = total_time
        job.save()
        
        # Convert matrix to base64 for transmission
        encrypted_b64 = base64.b64encode(encrypted_matrix.tobytes()).decode('utf-8')
        
        return Response({
            'job_id': job.job_id,
            'encrypted_data': encrypted_b64,
            'matrix_shape': encrypted_matrix.shape,
            'algorithm': algorithm,
            'processing_method': processing_method,
            'processing_time': total_time,
            'workers_used': num_workers if processing_method == 'parallel' else 1,
            'matrix_size': matrix_size
        })
        
    except Exception as e:
        if 'job' in locals():
            job.status = 'failed'
            job.error_message = str(e)
            job.save()
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([AllowAny])
def decrypt_text(request):
    """API endpoint for text decryption"""
    try:
        data = request.data
        encrypted_b64 = data.get('encrypted_data', '')
        matrix_shape = data.get('matrix_shape', [])
        algorithm = data.get('algorithm', 'hill_cipher')
        processing_method = data.get('processing_method', 'parallel')
        num_workers = data.get('num_workers', mp.cpu_count())
        matrix_size = data.get('matrix_size', 8)
        
        if not encrypted_b64:
            return Response({'error': 'No encrypted data provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Reconstruct matrix from base64
        encrypted_bytes = base64.b64decode(encrypted_b64)
        encrypted_matrix = np.frombuffer(encrypted_bytes).reshape(matrix_shape)
        
        # Initialize encryption service
        encryption_service = MatrixEncryptionService(algorithm=algorithm, matrix_size=matrix_size)
        
        start_time = time.time()
        
        if processing_method == 'serial':
            decrypted_text, processing_time = encryption_service.decrypt_serial(encrypted_matrix)
        else:
            decrypted_text, processing_time = encryption_service.decrypt_parallel(encrypted_matrix, num_workers=num_workers)
        
        total_time = time.time() - start_time
        
        return Response({
            'decrypted_text': decrypted_text,
            'algorithm': algorithm,
            'processing_method': processing_method,
            'processing_time': total_time,
            'workers_used': num_workers if processing_method == 'parallel' else 1
        })
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([AllowAny])
def benchmark_performance(request):
    """API endpoint for performance benchmarking"""
    try:
        data = request.data
        text = data.get('text', 'This is a comprehensive benchmark test for the matrix encryption service.')
        algorithm = data.get('algorithm', 'hill_cipher')
        iterations = data.get('iterations', 5)
        matrix_size = data.get('matrix_size', 8)
        
        encryption_service = MatrixEncryptionService(algorithm=algorithm, matrix_size=matrix_size)
        results = encryption_service.benchmark_performance(text, iterations=iterations)
        
        return Response({
            'benchmark_results': results,
            'algorithm': algorithm,
            'text_length': len(text),
            'iterations': iterations,
            'system_info': {
                'cpu_count': mp.cpu_count(),
                'matrix_size': matrix_size
            }
        })
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_job_status(request, job_id):
    """Get encryption job status"""
    try:
        job = EncryptionJob.objects.get(job_id=job_id)
        return Response({
            'job_id': job.job_id,
            'status': job.status,
            'algorithm': job.algorithm,
            'processing_method': job.processing_method,
            'processing_time': job.processing_time,
            'created_at': job.created_at,
            'completed_at': job.completed_at,
            'error_message': job.error_message
        })
    except EncryptionJob.DoesNotExist:
        return Response({'error': 'Job not found'}, status=status.HTTP_404_NOT_FOUND)
