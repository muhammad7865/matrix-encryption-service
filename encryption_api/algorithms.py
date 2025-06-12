import numpy as np
import time
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor
import base64

class MatrixEncryptionService:
    def __init__(self, algorithm='hill_cipher', matrix_size=8):
        self.algorithm = algorithm
        self.matrix_size = matrix_size
        self.key_matrix = self._generate_key_matrix()
        self.inv_key_matrix = self._calculate_inverse()

    def _generate_key_matrix(self):
        """Generate a simple, reliable key matrix"""
        np.random.seed(42)  # Fixed seed for reproducibility
        
        if self.algorithm == 'hill_cipher':
            # For Hill cipher, use a simple 2x2 matrix that we know works well
            # and extend it to the desired size
            base_matrix = np.array([
                [2, 3],
                [1, 4]
            ])
            
            # Extend to desired size
            if self.matrix_size <= 2:
                return base_matrix[:self.matrix_size, :self.matrix_size]
            else:
                extended = np.eye(self.matrix_size)
                for i in range(0, self.matrix_size, 2):
                    if i+1 < self.matrix_size:
                        extended[i:i+2, i:i+2] = base_matrix
                return extended
        
        elif self.algorithm == 'matrix_transform':
            # Simple transformation matrix
            matrix = np.eye(self.matrix_size) * 2
            for i in range(self.matrix_size):
                for j in range(self.matrix_size):
                    if i != j:
                        matrix[i, j] = 1
            return matrix
        
        else:  # advanced_matrix
            # Advanced but reliable matrix
            matrix = np.eye(self.matrix_size) * 3
            for i in range(self.matrix_size):
                matrix[i, (i + 1) % self.matrix_size] = 1
                matrix[i, (i - 1) % self.matrix_size] = 1
            return matrix

    def _calculate_inverse(self):
        """Calculate matrix inverse with better error handling"""
        try:
            if self.algorithm == 'hill_cipher':
                # For Hill cipher, we'll use a simpler approach
                # We know the inverse of our base 2x2 matrix
                base_inv = np.array([
                    [4, -3],
                    [-1, 2]
                ]) / 5  # Determinant is 5
                
                # Extend to desired size
                if self.matrix_size <= 2:
                    return base_inv[:self.matrix_size, :self.matrix_size]
                else:
                    extended = np.eye(self.matrix_size)
                    for i in range(0, self.matrix_size, 2):
                        if i+1 < self.matrix_size:
                            extended[i:i+2, i:i+2] = base_inv
                    return extended
            else:
                # For other algorithms, use standard inverse
                return np.linalg.inv(self.key_matrix)
        except:
            # Fallback to identity matrix
            return np.eye(self.matrix_size)

    def _prepare_text_simple(self, text):
        """Simple text preparation that preserves information"""
        if self.algorithm == 'hill_cipher':
            # For Hill cipher, we'll use a simpler approach
            # Convert text to ASCII values
            ascii_values = []
            for c in text:
                # Use values 0-127 for ASCII
                ascii_values.append(ord(c) % 128)
            
            # Pad to make divisible by matrix_size
            while len(ascii_values) % self.matrix_size != 0:
                ascii_values.append(32)  # Space character
        else:
            # For other algorithms, use the existing approach
            ascii_values = [ord(c) for c in text]
            while len(ascii_values) % self.matrix_size != 0:
                ascii_values.append(32)  # Space character
        
        # Reshape into matrix
        rows = len(ascii_values) // self.matrix_size
        return np.array(ascii_values).reshape(rows, self.matrix_size)

    def _restore_text_simple(self, matrix):
        """Simple text restoration"""
        # Round to integers and flatten
        ascii_values = np.round(matrix).astype(int).flatten()
        
        # Convert back to characters
        chars = []
        for val in ascii_values:
            if self.algorithm == 'hill_cipher':
                # For Hill cipher, ensure values are in valid ASCII range
                val = val % 128
                if val < 32:  # Not printable
                    val = 32  # Space
            else:
                # For other algorithms, ensure values are in valid range
                if val < 32:
                    val = 32
                elif val > 126:
                    val = val % 95 + 32
            
            chars.append(chr(val))
        
        return ''.join(chars).rstrip()

    def encrypt_serial(self, data, data_type='text'):
        """Simple, reliable serial encryption"""
        start_time = time.time()
        
        # Prepare data
        data_matrix = self._prepare_text_simple(data)
        
        # Apply encryption
        if self.algorithm == 'hill_cipher':
            # For Hill cipher, use a simpler approach
            encrypted_matrix = np.dot(data_matrix, self.key_matrix)
        else:
            encrypted_matrix = np.dot(data_matrix, self.key_matrix)
        
        processing_time = time.time() - start_time
        return encrypted_matrix, processing_time

    def decrypt_serial(self, encrypted_matrix, data_type='text'):
        """Simple, reliable serial decryption"""
        start_time = time.time()
        
        # Apply decryption
        if self.algorithm == 'hill_cipher':
            # For Hill cipher, use a simpler approach
            decrypted_matrix = np.dot(encrypted_matrix, self.inv_key_matrix)
        else:
            decrypted_matrix = np.dot(encrypted_matrix, self.inv_key_matrix)
        
        # Restore text
        result = self._restore_text_simple(decrypted_matrix)
        processing_time = time.time() - start_time
        
        return result, processing_time

    def encrypt_parallel(self, data, data_type='text', num_workers=None):
        """Parallel encryption"""
        if num_workers is None:
            num_workers = mp.cpu_count()
        
        start_time = time.time()
        data_matrix = self._prepare_text_simple(data)
        
        # For small data, use serial processing
        if data_matrix.shape[0] <= num_workers:
            return self.encrypt_serial(data, data_type)
        
        # Split into chunks
        chunks = np.array_split(data_matrix, num_workers)
        
        # Process chunks in parallel
        with ProcessPoolExecutor(max_workers=num_workers) as executor:
            futures = [executor.submit(self._encrypt_chunk, chunk) for chunk in chunks]
            results = [future.result() for future in futures]
        
        encrypted_matrix = np.vstack(results)
        processing_time = time.time() - start_time
        
        return encrypted_matrix, processing_time

    def _encrypt_chunk(self, chunk):
        """Encrypt a single chunk"""
        if self.algorithm == 'hill_cipher':
            return np.dot(chunk, self.key_matrix)
        else:
            return np.dot(chunk, self.key_matrix)

    def decrypt_parallel(self, encrypted_matrix, data_type='text', num_workers=None):
        """Parallel decryption"""
        if num_workers is None:
            num_workers = mp.cpu_count()
        
        start_time = time.time()
        
        # For small data, use serial processing
        if encrypted_matrix.shape[0] <= num_workers:
            return self.decrypt_serial(encrypted_matrix, data_type)
        
        # Split into chunks
        chunks = np.array_split(encrypted_matrix, num_workers)
        
        # Process chunks in parallel
        with ProcessPoolExecutor(max_workers=num_workers) as executor:
            futures = [executor.submit(self._decrypt_chunk, chunk) for chunk in chunks]
            results = [future.result() for future in futures]
        
        decrypted_matrix = np.vstack(results)
        result = self._restore_text_simple(decrypted_matrix)
        processing_time = time.time() - start_time
        
        return result, processing_time

    def _decrypt_chunk(self, chunk):
        """Decrypt a single chunk"""
        if self.algorithm == 'hill_cipher':
            return np.dot(chunk, self.inv_key_matrix)
        else:
            return np.dot(chunk, self.inv_key_matrix)

    def benchmark_performance(self, data, data_type='text', iterations=5):
        """Performance benchmark"""
        results = {}
        max_workers = mp.cpu_count()
        worker_counts = [1, 2, 4, max_workers] if max_workers >= 4 else [1, max_workers]
        
        for workers in worker_counts:
            times = []
            
            for _ in range(iterations):
                if workers == 1:
                    # Test serial encryption + decryption
                    start = time.time()
                    encrypted, _ = self.encrypt_serial(data, data_type)
                    decrypted, _ = self.decrypt_serial(encrypted, data_type)
                    times.append(time.time() - start)
                else:
                    # Test parallel encryption + decryption
                    start = time.time()
                    encrypted, _ = self.encrypt_parallel(data, data_type, workers)
                    decrypted, _ = self.decrypt_parallel(encrypted, data_type, workers)
                    times.append(time.time() - start)
            
            if workers == 1:
                results['serial'] = {
                    'avg_time': np.mean(times),
                    'std_time': np.std(times)
                }
            else:
                results[f'parallel_{workers}'] = {
                    'avg_time': np.mean(times),
                    'std_time': np.std(times),
                    'workers': workers
                }
        
        # Calculate speedup
        if 'serial' in results:
            serial_time = results['serial']['avg_time']
            for key in results:
                if key.startswith('parallel_'):
                    parallel_time = results[key]['avg_time']
                    results[key]['speedup'] = serial_time / parallel_time if parallel_time > 0 else 0
                    results[key]['efficiency'] = results[key]['speedup'] / results[key]['workers']
        
        return results
