from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import numpy as np
import time
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor
import hashlib
import base64
from django.conf import settings
import os

# Configure Django settings
if not settings.configured:
    settings.configure(
        DEBUG=True,
        SECRET_KEY='your-secret-key-here',
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'encryption_db.sqlite3',
            }
        },
        INSTALLED_APPS=[
            'django.contrib.contenttypes',
            'django.contrib.auth',
        ],
        USE_TZ=True,
    )

class MatrixEncryption:
    def __init__(self, key_size=8):
        self.key_size = key_size
        self.key_matrix = self._generate_key_matrix()
        self.inv_key_matrix = self._calculate_inverse()
    
    def _generate_key_matrix(self):
        """Generate a random invertible matrix for encryption"""
        np.random.seed(42)  # For reproducible results
        while True:
            matrix = np.random.randint(1, 10, (self.key_size, self.key_size))
            if np.linalg.det(matrix) != 0:  # Ensure matrix is invertible
                return matrix
    
    def _calculate_inverse(self):
        """Calculate the inverse matrix for decryption"""
        try:
            return np.linalg.inv(self.key_matrix).astype(float)
        except np.linalg.LinAlgError:
            return None
    
    def _text_to_matrix(self, text):
        """Convert text to matrix format"""
        # Pad text to make it divisible by key_size
        while len(text) % self.key_size != 0:
            text += ' '
        
        # Convert to ASCII values
        ascii_values = [ord(char) for char in text]
        
        # Reshape into matrix
        rows = len(ascii_values) // self.key_size
        return np.array(ascii_values).reshape(rows, self.key_size)
    
    def _matrix_to_text(self, matrix):
        """Convert matrix back to text"""
        ascii_values = matrix.flatten().astype(int)
        return ''.join(chr(max(32, min(126, val))) for val in ascii_values).rstrip()
    
    def encrypt_serial(self, plaintext):
        """Serial encryption using matrix multiplication"""
        text_matrix = self._text_to_matrix(plaintext)
        encrypted_matrix = np.dot(text_matrix, self.key_matrix)
        return encrypted_matrix
    
    def decrypt_serial(self, encrypted_matrix):
        """Serial decryption using inverse matrix"""
        decrypted_matrix = np.dot(encrypted_matrix, self.inv_key_matrix)
        return self._matrix_to_text(decrypted_matrix)
    
    def encrypt_parallel(self, plaintext, num_processes=None):
        """Parallel encryption using multiprocessing"""
        if num_processes is None:
            num_processes = mp.cpu_count()
        
        text_matrix = self._text_to_matrix(plaintext)
        
        # Split matrix into chunks for parallel processing
        chunks = np.array_split(text_matrix, num_processes)
        
        with ProcessPoolExecutor(max_workers=num_processes) as executor:
            futures = [executor.submit(self._encrypt_chunk, chunk) for chunk in chunks]
            results = [future.result() for future in futures]
        
        return np.vstack(results)
    
    def _encrypt_chunk(self, chunk):
        """Encrypt a chunk of the matrix"""
        return np.dot(chunk, self.key_matrix)
    
    def decrypt_parallel(self, encrypted_matrix, num_processes=None):
        """Parallel decryption using multiprocessing"""
        if num_processes is None:
            num_processes = mp.cpu_count()
        
        chunks = np.array_split(encrypted_matrix, num_processes)
        
        with ProcessPoolExecutor(max_workers=num_processes) as executor:
            futures = [executor.submit(self._decrypt_chunk, chunk) for chunk in chunks]
            results = [future.result() for future in futures]
        
        decrypted_matrix = np.vstack(results)
        return self._matrix_to_text(decrypted_matrix)
    
    def _decrypt_chunk(self, chunk):
        """Decrypt a chunk of the matrix"""
        return np.dot(chunk, self.inv_key_matrix)

def benchmark_encryption(text, iterations=10):
    """Benchmark serial vs parallel encryption performance"""
    encryptor = MatrixEncryption()
    
    # Serial benchmark
    serial_times = []
    for _ in range(iterations):
        start_time = time.time()
        encrypted = encryptor.encrypt_serial(text)
        decrypted = encryptor.decrypt_serial(encrypted)
        serial_times.append(time.time() - start_time)
    
    # Parallel benchmark
    parallel_times = []
    for _ in range(iterations):
        start_time = time.time()
        encrypted = encryptor.encrypt_parallel(text)
        decrypted = encryptor.decrypt_parallel(encrypted)
        parallel_times.append(time.time() - start_time)
    
    return {
        'serial_avg': np.mean(serial_times),
        'parallel_avg': np.mean(parallel_times),
        'speedup': np.mean(serial_times) / np.mean(parallel_times),
        'cpu_count': mp.cpu_count()
    }

def index(request):
    """Main page view"""
    return render(request, 'index.html')

@csrf_exempt
def encrypt_text(request):
    """API endpoint for text encryption"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            text = data.get('text', '')
            method = data.get('method', 'serial')
            
            if not text:
                return JsonResponse({'error': 'No text provided'}, status=400)
            
            encryptor = MatrixEncryption()
            start_time = time.time()
            
            if method == 'serial':
                encrypted_matrix = encryptor.encrypt_serial(text)
            else:
                encrypted_matrix = encryptor.encrypt_parallel(text)
            
            encryption_time = time.time() - start_time
            
            # Convert matrix to base64 for transmission
            encrypted_b64 = base64.b64encode(encrypted_matrix.tobytes()).decode('utf-8')
            
            return JsonResponse({
                'encrypted': encrypted_b64,
                'matrix_shape': encrypted_matrix.shape,
                'encryption_time': encryption_time,
                'method': method
            })
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def decrypt_text(request):
    """API endpoint for text decryption"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            encrypted_b64 = data.get('encrypted', '')
            matrix_shape = data.get('matrix_shape', [])
            method = data.get('method', 'serial')
            
            if not encrypted_b64:
                return JsonResponse({'error': 'No encrypted data provided'}, status=400)
            
            # Reconstruct matrix from base64
            encrypted_bytes = base64.b64decode(encrypted_b64)
            encrypted_matrix = np.frombuffer(encrypted_bytes).reshape(matrix_shape)
            
            encryptor = MatrixEncryption()
            start_time = time.time()
            
            if method == 'serial':
                decrypted_text = encryptor.decrypt_serial(encrypted_matrix)
            else:
                decrypted_text = encryptor.decrypt_parallel(encrypted_matrix)
            
            decryption_time = time.time() - start_time
            
            return JsonResponse({
                'decrypted': decrypted_text,
                'decryption_time': decryption_time,
                'method': method
            })
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def benchmark(request):
    """API endpoint for performance benchmarking"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            text = data.get('text', 'This is a sample text for benchmarking the matrix encryption system.')
            iterations = data.get('iterations', 5)
            
            results = benchmark_encryption(text, iterations)
            
            return JsonResponse({
                'benchmark_results': results,
                'text_length': len(text),
                'iterations': iterations
            })
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

# URL patterns
from django.urls import path
urlpatterns = [
    path('', index, name='index'),
    path('api/encrypt/', encrypt_text, name='encrypt'),
    path('api/decrypt/', decrypt_text, name='decrypt'),
    path('api/benchmark/', benchmark, name='benchmark'),
]

# Django application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
