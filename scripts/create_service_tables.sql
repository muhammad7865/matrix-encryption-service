-- Create comprehensive database schema for Encryption-as-a-Service

-- Users table (extends Django's auth_user)
CREATE TABLE IF NOT EXISTS authentication_user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    password VARCHAR(128) NOT NULL,
    last_login DATETIME,
    is_superuser BOOLEAN NOT NULL,
    username VARCHAR(150) UNIQUE NOT NULL,
    first_name VARCHAR(150) NOT NULL,
    last_name VARCHAR(150) NOT NULL,
    email VARCHAR(254) UNIQUE NOT NULL,
    is_staff BOOLEAN NOT NULL,
    is_active BOOLEAN NOT NULL,
    date_joined DATETIME NOT NULL,
    company VARCHAR(200) NOT NULL,
    api_usage_limit INTEGER NOT NULL,
    is_premium BOOLEAN NOT NULL,
    created_at DATETIME NOT NULL
);

-- API Keys table
CREATE TABLE IF NOT EXISTS authentication_apikey (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    key VARCHAR(64) UNIQUE NOT NULL,
    is_active BOOLEAN NOT NULL,
    usage_count INTEGER NOT NULL,
    last_used DATETIME,
    created_at DATETIME NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES authentication_user (id)
);

-- Service Usage tracking
CREATE TABLE IF NOT EXISTS authentication_serviceusage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    operation_type VARCHAR(50) NOT NULL,
    algorithm_used VARCHAR(50) NOT NULL,
    processing_method VARCHAR(20) NOT NULL,
    data_size INTEGER NOT NULL,
    processing_time REAL NOT NULL,
    cpu_cores_used INTEGER NOT NULL,
    timestamp DATETIME NOT NULL,
    success BOOLEAN NOT NULL,
    error_message TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    api_key_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES authentication_user (id),
    FOREIGN KEY (api_key_id) REFERENCES authentication_apikey (id)
);

-- Encryption Jobs table
CREATE TABLE IF NOT EXISTS encryption_api_encryptionjob (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id VARCHAR(32) UNIQUE NOT NULL,
    algorithm VARCHAR(50) NOT NULL,
    processing_method VARCHAR(20) NOT NULL,
    status VARCHAR(20) NOT NULL,
    input_type VARCHAR(20) NOT NULL,
    input_size INTEGER NOT NULL,
    matrix_size INTEGER NOT NULL,
    parallel_workers INTEGER NOT NULL,
    processing_time REAL,
    speedup_factor REAL,
    created_at DATETIME NOT NULL,
    completed_at DATETIME,
    error_message TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES authentication_user (id)
);

-- Encrypted Files table
CREATE TABLE IF NOT EXISTS encryption_api_encryptedfile (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    original_filename VARCHAR(255) NOT NULL,
    encrypted_file VARCHAR(100) NOT NULL,
    encryption_key_hash VARCHAR(64) NOT NULL,
    file_size INTEGER NOT NULL,
    created_at DATETIME NOT NULL,
    job_id INTEGER NOT NULL,
    FOREIGN KEY (job_id) REFERENCES encryption_api_encryptionjob (id)
);

-- System Metrics table
CREATE TABLE IF NOT EXISTS analytics_systemmetrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME NOT NULL,
    cpu_usage REAL NOT NULL,
    memory_usage REAL NOT NULL,
    active_jobs INTEGER NOT NULL,
    total_requests INTEGER NOT NULL,
    average_response_time REAL NOT NULL
);

-- Algorithm Performance table
CREATE TABLE IF NOT EXISTS analytics_algorithmperformance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    algorithm VARCHAR(50) NOT NULL,
    matrix_size INTEGER NOT NULL,
    avg_serial_time REAL NOT NULL,
    avg_parallel_time REAL NOT NULL,
    max_speedup REAL NOT NULL,
    optimal_workers INTEGER NOT NULL,
    last_updated DATETIME NOT NULL
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_apikey_user ON authentication_apikey(user_id);
CREATE INDEX IF NOT EXISTS idx_apikey_key ON authentication_apikey(key);
CREATE INDEX IF NOT EXISTS idx_usage_user ON authentication_serviceusage(user_id);
CREATE INDEX IF NOT EXISTS idx_usage_timestamp ON authentication_serviceusage(timestamp);
CREATE INDEX IF NOT EXISTS idx_job_user ON encryption_api_encryptionjob(user_id);
CREATE INDEX IF NOT EXISTS idx_job_status ON encryption_api_encryptionjob(status);
CREATE INDEX IF NOT EXISTS idx_job_algorithm ON encryption_api_encryptionjob(algorithm);
CREATE INDEX IF NOT EXISTS idx_file_job ON encryption_api_encryptedfile(job_id);
CREATE INDEX IF NOT EXISTS idx_metrics_timestamp ON analytics_systemmetrics(timestamp);
CREATE INDEX IF NOT EXISTS idx_performance_algorithm ON analytics_algorithmperformance(algorithm);
