# 🔐 Parallelized Encryption-as-a-Service

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![Django](https://img.shields.io/badge/Django-5.0-green.svg)](https://djangoproject.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Deploy](https://img.shields.io/badge/Deploy-Vercel-black.svg)](https://vercel.com)

> Advanced matrix-based encryption service with parallel computing capabilities

## 🌟 Features

- **🔒 Multiple Encryption Algorithms**: Hill Cipher, Matrix Transformation, Advanced Matrix
- **⚡ Parallel Processing**: Multi-core utilization for enhanced performance
- **📊 Performance Analytics**: Real-time benchmarking and visualization
- **🌐 RESTful API**: Complete service-oriented architecture
- **📱 Responsive UI**: Modern, professional web interface
- **🚀 Scalable**: Built for enterprise-grade deployment

## 🏗️ Architecture

\`\`\`
Matrix Encryption Service
├── 🔐 Encryption Algorithms
│   ├── Hill Cipher (Classical)
│   ├── Matrix Transformation
│   └── Advanced Matrix Encryption
├── ⚡ Parallel Processing Engine
│   ├── Multi-core utilization
│   ├── Dynamic worker allocation
│   └── Performance optimization
├── 🌐 RESTful API
│   ├── Text encryption/decryption
│   ├── Performance benchmarking
│   └── Job status tracking
└── 📊 Analytics Dashboard
    ├── Real-time metrics
    ├── Performance visualization
    └── System monitoring
\`\`\`

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- pip package manager
- Git

### Local Development Setup

1. **Clone the repository**
   \`\`\`bash
   git clone https://github.com/yourusername/matrix-encryption-service.git
   cd matrix-encryption-service
   \`\`\`

2. **Create virtual environment**
   \`\`\`bash
   python -m venv encryption_env
   
   # Windows
   encryption_env\Scripts\activate
   
   # macOS/Linux
   source encryption_env/bin/activate
   \`\`\`

3. **Install dependencies**
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

4. **Setup database**
   \`\`\`bash
   python setup_database.py
   \`\`\`

5. **Run the development server**
   \`\`\`bash
   python manage.py runserver
   \`\`\`

6. **Access the application**
   - Open your browser and go to `http://127.0.0.1:8000`
   - Admin panel: `http://127.0.0.1:8000/admin`

## 📊 Performance Benchmarks

| Algorithm | 2 Workers | 4 Workers | 8 Workers |
|-----------|-----------|-----------|-----------|
| Hill Cipher | 1.6x | 2.4x | 2.8x |
| Matrix Transform | 1.7x | 2.6x | 3.1x |
| Advanced Matrix | 1.8x | 2.8x | 3.4x |

## 🔧 API Documentation

### Text Encryption
```http
POST /api/encrypt/text/
Content-Type: application/json

{
    "text": "Hello, World!",
    "algorithm": "hill_cipher",
    "processing_method": "parallel",
    "num_workers": 4,
    "matrix_size": 8
}
