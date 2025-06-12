-- Insert sample data for demonstration

-- Sample encryption operations
INSERT INTO encryption_operations (original_text, encrypted_data, matrix_shape, encryption_method, encryption_time) VALUES
('Hello World!', 'sample_encrypted_data_1', '[2, 8]', 'serial', 0.0023),
('This is a test message for matrix encryption.', 'sample_encrypted_data_2', '[6, 8]', 'parallel', 0.0015),
('Matrix-based encryption with parallel processing.', 'sample_encrypted_data_3', '[7, 8]', 'serial', 0.0034),
('Advanced cryptographic operations using linear algebra.', 'sample_encrypted_data_4', '[8, 8]', 'parallel', 0.0019);

-- Sample decryption operations
INSERT INTO decryption_operations (encrypted_data, decrypted_text, decryption_method, decryption_time) VALUES
('sample_encrypted_data_1', 'Hello World!', 'serial', 0.0021),
('sample_encrypted_data_2', 'This is a test message for matrix encryption.', 'parallel', 0.0013),
('sample_encrypted_data_3', 'Matrix-based encryption with parallel processing.', 'serial', 0.0031),
('sample_encrypted_data_4', 'Advanced cryptographic operations using linear algebra.', 'parallel', 0.0017);

-- Sample benchmark results
INSERT INTO benchmark_results (text_length, iterations, serial_avg_time, parallel_avg_time, speedup_factor, cpu_count) VALUES
(100, 10, 0.0025, 0.0015, 1.67, 4),
(500, 10, 0.0089, 0.0045, 1.98, 4),
(1000, 10, 0.0156, 0.0067, 2.33, 4),
(2000, 10, 0.0298, 0.0112, 2.66, 4),
(5000, 10, 0.0723, 0.0234, 3.09, 4);

-- Sample performance metrics
INSERT INTO performance_metrics (operation_type, processing_method, text_length, processing_time, cpu_cores_used) VALUES
('encryption', 'serial', 256, 0.0045, 1),
('encryption', 'parallel', 256, 0.0023, 4),
('decryption', 'serial', 256, 0.0041, 1),
('decryption', 'parallel', 256, 0.0021, 4),
('encryption', 'serial', 1024, 0.0167, 1),
('encryption', 'parallel', 1024, 0.0067, 4),
('decryption', 'serial', 1024, 0.0154, 1),
('decryption', 'parallel', 1024, 0.0063, 4);
