-- Insert sample data for the Encryption-as-a-Service platform

-- Sample users
INSERT INTO authentication_user (
    password, username, first_name, last_name, email, is_staff, is_active, 
    date_joined, company, api_usage_limit, is_premium, created_at
) VALUES
('pbkdf2_sha256$260000$sample', 'demo_user', 'Demo', 'User', 'demo@example.com', 
 0, 1, datetime('now'), 'Demo Company', 1000, 0, datetime('now')),
('pbkdf2_sha256$260000$sample', 'enterprise_user', 'Enterprise', 'User', 'enterprise@example.com', 
 0, 1, datetime('now'), 'Enterprise Corp', 10000, 1, datetime('now')),
('pbkdf2_sha256$260000$sample', 'researcher', 'Research', 'User', 'research@university.edu', 
 0, 1, datetime('now'), 'University Research Lab', 5000, 1, datetime('now'));

-- Sample API keys
INSERT INTO authentication_apikey (name, key, is_active, usage_count, created_at, user_id) VALUES
('Demo API Key', 'eaas_demo123456789abcdef', 1, 45, datetime('now'), 1),
('Production Key', 'eaas_prod987654321fedcba', 1, 234, datetime('now'), 2),
('Research Key', 'eaas_research456789123abc', 1, 89, datetime('now'), 3),
('Backup Key', 'eaas_backup789123456def', 1, 12, datetime('now'), 2);

-- Sample encryption jobs
INSERT INTO encryption_api_encryptionjob (
    job_id, algorithm, processing_method, status, input_type, input_size, 
    matrix_size, parallel_workers, processing_time, speedup_factor, 
    created_at, completed_at, error_message, user_id
) VALUES
('job001', 'hill_cipher', 'parallel', 'completed', 'text', 256, 8, 4, 0.0234, 2.1, 
 datetime('now', '-2 hours'), datetime('now', '-2 hours'), '', 1),
('job002', 'matrix_transform', 'serial', 'completed', 'file', 1048576, 8, 1, 0.456, 1.0, 
 datetime('now', '-1 hour'), datetime('now', '-1 hour'), '', 2),
('job003', 'advanced_matrix', 'parallel', 'completed', 'text', 512, 16, 8, 0.0189, 3.2, 
 datetime('now', '-30 minutes'), datetime('now', '-30 minutes'), '', 3),
('job004', 'hill_cipher', 'parallel', 'processing', 'file', 2097152, 8, 4, NULL, NULL, 
 datetime('now', '-5 minutes'), NULL, '', 1),
('job005', 'matrix_transform', 'parallel', 'failed', 'text', 128, 8, 4, NULL, NULL, 
 datetime('now', '-10 minutes'), NULL, 'Matrix inversion failed', 2);

-- Sample service usage data
INSERT INTO authentication_serviceusage (
    operation_type, algorithm_used, processing_method, data_size, processing_time, 
    cpu_cores_used, timestamp, success, error_message, user_id, api_key_id
) VALUES
('encrypt_text', 'hill_cipher', 'parallel', 256, 0.0234, 4, datetime('now', '-2 hours'), 1, '', 1, 1),
('decrypt_text', 'hill_cipher', 'parallel', 256, 0.0198, 4, datetime('now', '-2 hours'), 1, '', 1, 1),
('encrypt_file', 'matrix_transform', 'serial', 1048576, 0.456, 1, datetime('now', '-1 hour'), 1, '', 2, 2),
('benchmark', 'advanced_matrix', 'mixed', 512, 0.234, 8, datetime('now', '-30 minutes'), 1, '', 3, 3),
('encrypt_text', 'hill_cipher', 'parallel', 128, 0.0156, 4, datetime('now', '-20 minutes'), 1, '', 1, 1),
('encrypt_file', 'matrix_transform', 'parallel', 2097152, 0.789, 8, datetime('now', '-15 minutes'), 1, '', 2, 2),
('decrypt_text', 'advanced_matrix', 'parallel', 512, 0.0234, 8, datetime('now', '-10 minutes'), 1, '', 3, 3),
('benchmark', 'hill_cipher', 'mixed', 1024, 0.345, 4, datetime('now', '-5 minutes'), 1, '', 1, 1);

-- Sample encrypted files
INSERT INTO encryption_api_encryptedfile (
    original_filename, encrypted_file, encryption_key_hash, file_size, created_at, job_id
) VALUES
('document.pdf', 'encrypted/job002.npy', 'hash123456789abcdef', 1048576, datetime('now', '-1 hour'), 2),
('image.jpg', 'encrypted/job004.npy', 'hash987654321fedcba', 2097152, datetime('now', '-5 minutes'), 4);

-- Sample system metrics
INSERT INTO analytics_systemmetrics (
    timestamp, cpu_usage, memory_usage, active_jobs, total_requests, average_response_time
) VALUES
(datetime('now', '-1 hour'), 45.2, 67.8, 3, 156, 0.234),
(datetime('now', '-50 minutes'), 52.1, 71.2, 5, 189, 0.198),
(datetime('now', '-40 minutes'), 38.9, 64.5, 2, 167, 0.267),
(datetime('now', '-30 minutes'), 61.3, 78.9, 7, 234, 0.189),
(datetime('now', '-20 minutes'), 43.7, 69.1, 4, 198, 0.223),
(datetime('now', '-10 minutes'), 55.8, 73.4, 6, 267, 0.201),
(datetime('now'), 48.2, 70.6, 3, 189, 0.245);

-- Sample algorithm performance data
INSERT INTO analytics_algorithmperformance (
    algorithm, matrix_size, avg_serial_time, avg_parallel_time, max_speedup, optimal_workers, last_updated
) VALUES
('hill_cipher', 8, 0.0456, 0.0189, 2.41, 4, datetime('now')),
('hill_cipher', 16, 0.1234, 0.0398, 3.10, 8, datetime('now')),
('matrix_transform', 8, 0.0567, 0.0234, 2.42, 4, datetime('now')),
('matrix_transform', 16, 0.1456, 0.0456, 3.19, 8, datetime('now')),
('advanced_matrix', 8, 0.0678, 0.0198, 3.42, 8, datetime('now')),
('advanced_matrix', 16, 0.1678, 0.0398, 4.21, 8, datetime('now'));
