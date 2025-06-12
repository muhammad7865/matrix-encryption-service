import numpy as np
import matplotlib.pyplot as plt
import time
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor

class PerformanceAnalyzer:
    def __init__(self):
        self.results = []
    
    def analyze_scalability(self, text_sizes, max_processes=None):
        """Analyze performance scalability across different text sizes and process counts"""
        if max_processes is None:
            max_processes = mp.cpu_count()
        
        print("Performance Scalability Analysis")
        print("=" * 50)
        
        for size in text_sizes:
            # Generate test text
            test_text = "A" * size
            
            print(f"\nAnalyzing text size: {size} characters")
            
            # Test different process counts
            for processes in range(1, max_processes + 1):
                serial_time = self.benchmark_serial(test_text)
                parallel_time = self.benchmark_parallel(test_text, processes)
                
                speedup = serial_time / parallel_time if parallel_time > 0 else 0
                efficiency = speedup / processes
                
                result = {
                    'text_size': size,
                    'processes': processes,
                    'serial_time': serial_time,
                    'parallel_time': parallel_time,
                    'speedup': speedup,
                    'efficiency': efficiency
                }
                
                self.results.append(result)
                
                print(f"  Processes: {processes:2d} | "
                      f"Serial: {serial_time:.4f}s | "
                      f"Parallel: {parallel_time:.4f}s | "
                      f"Speedup: {speedup:.2f}x | "
                      f"Efficiency: {efficiency:.2f}")
    
    def benchmark_serial(self, text):
        """Benchmark serial matrix operations"""
        start_time = time.time()
        
        # Simulate matrix encryption operations
        matrix_size = len(text) // 8 + 1
        matrix = np.random.rand(matrix_size, 8)
        key_matrix = np.random.rand(8, 8)
        
        # Matrix multiplication
        result = np.dot(matrix, key_matrix)
        
        return time.time() - start_time
    
    def benchmark_parallel(self, text, num_processes):
        """Benchmark parallel matrix operations"""
        start_time = time.time()
        
        # Simulate matrix encryption operations
        matrix_size = len(text) // 8 + 1
        matrix = np.random.rand(matrix_size, 8)
        key_matrix = np.random.rand(8, 8)
        
        # Split matrix for parallel processing
        chunks = np.array_split(matrix, num_processes)
        
        with ProcessPoolExecutor(max_workers=num_processes) as executor:
            futures = [executor.submit(self._process_chunk, chunk, key_matrix) for chunk in chunks]
            results = [future.result() for future in futures]
        
        return time.time() - start_time
    
    def _process_chunk(self, chunk, key_matrix):
        """Process a chunk of the matrix"""
        return np.dot(chunk, key_matrix)
    
    def generate_report(self):
        """Generate a comprehensive performance report"""
        if not self.results:
            print("No results to analyze. Run analyze_scalability first.")
            return
        
        print("\n" + "=" * 60)
        print("COMPREHENSIVE PERFORMANCE ANALYSIS REPORT")
        print("=" * 60)
        
        # Group results by text size
        text_sizes = sorted(set(r['text_size'] for r in self.results))
        
        for size in text_sizes:
            size_results = [r for r in self.results if r['text_size'] == size]
            
            print(f"\nText Size: {size} characters")
            print("-" * 40)
            
            best_speedup = max(r['speedup'] for r in size_results)
            best_processes = next(r['processes'] for r in size_results if r['speedup'] == best_speedup)
            
            print(f"Best speedup: {best_speedup:.2f}x with {best_processes} processes")
            
            # Calculate parallel efficiency
            max_processes = max(r['processes'] for r in size_results)
            max_efficiency = max(r['efficiency'] for r in size_results)
            
            print(f"Maximum efficiency: {max_efficiency:.2f} ({max_efficiency*100:.1f}%)")
            print(f"Scalability up to {max_processes} processes")
        
        # Overall statistics
        print(f"\nOverall Statistics:")
        print("-" * 20)
        avg_speedup = np.mean([r['speedup'] for r in self.results if r['processes'] > 1])
        max_speedup = max(r['speedup'] for r in self.results)
        
        print(f"Average speedup: {avg_speedup:.2f}x")
        print(f"Maximum speedup achieved: {max_speedup:.2f}x")
        
        # Recommendations
        print(f"\nRecommendations:")
        print("-" * 15)
        
        optimal_processes = {}
        for size in text_sizes:
            size_results = [r for r in self.results if r['text_size'] == size]
            best = max(size_results, key=lambda x: x['speedup'])
            optimal_processes[size] = best['processes']
        
        for size, processes in optimal_processes.items():
            print(f"Text size {size}: Use {processes} processes for optimal performance")

# Run the analysis
if __name__ == "__main__":
    analyzer = PerformanceAnalyzer()
    
    # Test different text sizes
    text_sizes = [100, 500, 1000, 2000, 5000]
    
    print(f"Starting performance analysis on {mp.cpu_count()} CPU cores...")
    analyzer.analyze_scalability(text_sizes)
    analyzer.generate_report()
    
    print(f"\nAnalysis complete! Results saved for {len(analyzer.results)} test cases.")
