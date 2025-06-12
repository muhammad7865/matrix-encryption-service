-- Create database tables for the matrix encryption system

-- Table to store encryption operations
CREATE TABLE IF NOT EXISTS encryption_operations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    original_text TEXT NOT NULL,
    encrypted_data TEXT NOT NULL,
    matrix_shape TEXT NOT NULL,
    encryption_method VARCHAR(20) NOT NULL,
    encryption_time REAL NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table to store decryption operations
CREATE TABLE IF NOT EXISTS decryption_operations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    encrypted_data TEXT NOT NULL,
    decrypted_text TEXT NOT NULL,
    decryption_method VARCHAR(20) NOT NULL,
    decryption_time REAL NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table to store benchmark results
CREATE TABLE IF NOT EXISTS benchmark_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text_length INTEGER NOT NULL,
    iterations INTEGER NOT NULL,
    serial_avg_time REAL NOT NULL,
    parallel_avg_time REAL NOT NULL,
    speedup_factor REAL NOT NULL,
    cpu_count INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table to store system performance metrics
CREATE TABLE IF NOT EXISTS performance_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    operation_type VARCHAR(20) NOT NULL,
    processing_method VARCHAR(20) NOT NULL,
    text_length INTEGER NOT NULL,
    processing_time REAL NOT NULL,
    cpu_cores_used INTEGER,
    memory_usage REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_encryption_method ON encryption_operations(encryption_method);
CREATE INDEX IF NOT EXISTS idx_decryption_method ON decryption_operations(decryption_method);
CREATE INDEX IF NOT EXISTS idx_benchmark_created ON benchmark_results(created_at);
CREATE INDEX IF NOT EXISTS idx_performance_operation ON performance_metrics(operation_type, processing_method);
