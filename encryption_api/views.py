from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
import json
import uuid
import time
import multiprocessing as mp
from .algorithms import MatrixEncryptionService
from .models import EncryptionJob
import numpy as np
import base64

def dashboard(request):
    """Main dashboard view"""
    return render(request, 'dashboard.html')

@api_view(['POST'])
@permission_classes([AllowAny])
def encrypt_text(request):
    """Enhanced API endpoint for text encryption with proper worker handling"""
    try:
        data = request.data
        text = data.get('text', '')
        algorithm = data.get('algorithm', 'hill_cipher')
        processing_method = data.get('processing_method', 'parallel')
        num_workers = data.get('num_workers', mp.cpu_count())
        matrix_size = data.get('matrix_size', 8)
        
        # Ensure valid worker count
        num_workers = max(1, min(int(num_workers), mp.cpu_count()))
        
        print(f"\n🔐 ENCRYPTION REQUEST:")
        print(f"   Text length: {len(text):,} characters")
        print(f"   Algorithm: {algorithm}")
        print(f"   Requested method: {processing_method}")
        print(f"   Requested workers: {num_workers}")
        
        if not text:
            return Response({'error': 'No text provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create encryption job
        job = EncryptionJob.objects.create(
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
        
        # Call the appropriate method
        if processing_method == 'serial':
            encrypted_matrix, processing_stats = encryption_service.encrypt_serial(text)
            actual_method = 'serial'
            actual_workers = 1
        else:
            encrypted_matrix, processing_stats = encryption_service.encrypt_parallel(text, num_workers)
            actual_method = 'parallel'
            actual_workers = processing_stats.get('workers', num_workers)
        
        total_time = time.time() - start_time
        
        print(f"✅ Encryption completed:")
        print(f"   Method: {actual_method} ({actual_workers} workers)")
        print(f"   Time: {total_time:.4f}s")
        
        # Update job status
        job.status = 'completed'
        job.processing_time = total_time
        job.processing_method = actual_method
        job.parallel_workers = actual_workers
        job.save()
        
        # Convert matrix to base64 for transmission
        encrypted_b64 = base64.b64encode(encrypted_matrix.tobytes()).decode('utf-8')
        
        return Response({
            'job_id': job.job_id,
            'encrypted_data': encrypted_b64,
            'matrix_shape': encrypted_matrix.shape,
            'algorithm': algorithm,
            'processing_method': actual_method,
            'processing_time': total_time,
            'workers_used': actual_workers,
            'workers_requested': num_workers,
            'matrix_size': matrix_size,
            'data_size': len(text),
            'processing_stats': processing_stats
        })
        
    except Exception as e:
        print(f"❌ Encryption error: {e}")
        if 'job' in locals():
            job.status = 'failed'
            job.error_message = str(e)
            job.save()
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([AllowAny])
def decrypt_text(request):
    """Enhanced API endpoint for text decryption with proper worker handling"""
    try:
        data = request.data
        encrypted_b64 = data.get('encrypted_data', '')
        matrix_shape = data.get('matrix_shape', [])
        algorithm = data.get('algorithm', 'hill_cipher')
        processing_method = data.get('processing_method', 'parallel')
        num_workers = data.get('num_workers', mp.cpu_count())
        matrix_size = data.get('matrix_size', 8)
        
        # Ensure valid worker count
        num_workers = max(1, min(int(num_workers), mp.cpu_count()))
        
        print(f"\n🔓 DECRYPTION REQUEST:")
        print(f"   Matrix shape: {matrix_shape}")
        print(f"   Algorithm: {algorithm}")
        print(f"   Requested method: {processing_method}")
        print(f"   Requested workers: {num_workers}")
        
        if not encrypted_b64:
            return Response({'error': 'No encrypted data provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Reconstruct matrix from base64
        encrypted_bytes = base64.b64decode(encrypted_b64)
        encrypted_matrix = np.frombuffer(encrypted_bytes).reshape(matrix_shape)
        
        # Initialize encryption service
        encryption_service = MatrixEncryptionService(algorithm=algorithm, matrix_size=matrix_size)
        
        start_time = time.time()
        
        # Call the appropriate method
        if processing_method == 'serial':
            decrypted_text, processing_stats = encryption_service.decrypt_serial(encrypted_matrix)
            actual_method = 'serial'
            actual_workers = 1
        else:
            decrypted_text, processing_stats = encryption_service.decrypt_parallel(encrypted_matrix, num_workers)
            actual_method = 'parallel'
            actual_workers = processing_stats.get('workers', num_workers)
        
        total_time = time.time() - start_time
        
        print(f"✅ Decryption completed:")
        print(f"   Method: {actual_method} ({actual_workers} workers)")
        print(f"   Time: {total_time:.4f}s")
        
        return Response({
            'decrypted_text': decrypted_text,
            'algorithm': algorithm,
            'processing_method': actual_method,
            'processing_time': total_time,
            'workers_used': actual_workers,
            'workers_requested': num_workers,
            'matrix_rows': encrypted_matrix.shape[0],
            'processing_stats': processing_stats
        })
        
    except Exception as e:
        print(f"❌ Decryption error: {e}")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([AllowAny])
def benchmark_performance(request):
    """Enhanced API endpoint for performance benchmarking"""
    try:
        data = request.data
        text = data.get('text', 'This is a comprehensive benchmark test for the matrix encryption service.')
        algorithm = data.get('algorithm', 'hill_cipher')
        iterations = data.get('iterations', 3)
        matrix_size = data.get('matrix_size', 8)
        num_workers = data.get('num_workers', mp.cpu_count())
        
        # Ensure valid parameters
        #iterations = max(1, min(int(iterations), 10))
        iterations = max(1, int(iterations))  # Remove upper limit, only ensure minimum of 1
        num_workers = max(1, min(int(num_workers), mp.cpu_count()))
        
        print(f"\n🔬 ENHANCED BENCHMARK REQUEST:")
        print(f"   Text length: {len(text):,} characters")
        print(f"   Algorithm: {algorithm}")
        print(f"   Iterations: {iterations}")
        print(f"   Matrix size: {matrix_size}")
        print(f"   Requested workers: {num_workers}")
        
        encryption_service = MatrixEncryptionService(algorithm=algorithm, matrix_size=matrix_size)
        results = encryption_service.benchmark_performance(text, iterations=iterations, num_workers=num_workers)
        
        return Response({
            'benchmark_results': results,
            'algorithm': algorithm,
            'text_length': len(text),
            'iterations': iterations,
            'requested_workers': num_workers,
            'system_info': {
                'cpu_count': mp.cpu_count(),
                'matrix_size': matrix_size,
                'parallel_threshold': encryption_service.config['parallel_threshold'],
                'algorithm_complexity': encryption_service.config['complexity_score']
            }
        })
        
    except Exception as e:
        print(f"❌ Benchmark error: {e}")
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
            'parallel_workers': job.parallel_workers,
            'created_at': job.created_at,
            'completed_at': job.completed_at,
            'error_message': job.error_message
        })
    except EncryptionJob.DoesNotExist:
        return Response({'error': 'Job not found'}, status=status.HTTP_404_NOT_FOUND)
