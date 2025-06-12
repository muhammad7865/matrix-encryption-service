#!/usr/bin/env python
"""
Database setup script for Matrix Encryption Service
Run this script to create and populate the database tables
"""

import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'encryption_service.settings')

try:
    django.setup()
except Exception as e:
    print(f"Error setting up Django: {e}")
    sys.exit(1)

from django.core.management import execute_from_command_line
from django.db import connection
import sqlite3

def run_sql_file(file_path):
    """Execute SQL commands from a file"""
    try:
        with open(file_path, 'r') as file:
            sql_content = file.read()
        
        # Split SQL commands by semicolon and execute each
        commands = [cmd.strip() for cmd in sql_content.split(';') if cmd.strip()]
        
        with connection.cursor() as cursor:
            for command in commands:
                if command:
                    try:
                        cursor.execute(command)
                        print(f"✅ Executed: {command[:50]}...")
                    except Exception as e:
                        print(f"❌ Error executing command: {e}")
        
        print(f"✅ Successfully executed SQL file: {file_path}")
        
    except FileNotFoundError:
        print(f"❌ SQL file not found: {file_path}")
    except Exception as e:
        print(f"❌ Error executing SQL file {file_path}: {e}")

def setup_database():
    """Complete database setup process"""
    print("🚀 Starting Matrix Encryption Service Database Setup")
    print("=" * 60)
    
    # Step 1: Create Django migrations
    print("\n📋 Step 1: Creating Django migrations...")
    try:
        execute_from_command_line(['manage.py', 'makemigrations'])
        print("✅ Migrations created successfully")
    except Exception as e:
        print(f"❌ Error creating migrations: {e}")
    
    # Step 2: Apply migrations
    print("\n📋 Step 2: Applying migrations...")
    try:
        execute_from_command_line(['manage.py', 'migrate'])
        print("✅ Migrations applied successfully")
    except Exception as e:
        print(f"❌ Error applying migrations: {e}")
    
    # Step 3: Run custom SQL scripts
    print("\n📋 Step 3: Running custom SQL scripts...")
    
    sql_files = [
        'scripts/create_tables.sql',
        'scripts/seed_sample_data.sql',
        'scripts/create_service_tables.sql',
        'scripts/seed_service_data.sql'
    ]
    
    for sql_file in sql_files:
        if os.path.exists(sql_file):
            print(f"\n🔄 Running {sql_file}...")
            run_sql_file(sql_file)
        else:
            print(f"⚠️  SQL file not found: {sql_file}")
    
    # Step 4: Create superuser (optional)
    print("\n📋 Step 4: Creating superuser (optional)...")
    create_superuser = input("Do you want to create a superuser? (y/n): ").lower().strip()
    
    if create_superuser == 'y':
        try:
            execute_from_command_line(['manage.py', 'createsuperuser'])
            print("✅ Superuser created successfully")
        except Exception as e:
            print(f"❌ Error creating superuser: {e}")
    
    print("\n🎉 Database setup completed!")
    print("=" * 60)
    print("📊 Database Summary:")
    
    # Display table information
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            print(f"📋 Total tables created: {len(tables)}")
            for table in tables:
                print(f"   • {table[0]}")
    except Exception as e:
        print(f"❌ Error getting table info: {e}")
    
    print("\n🚀 You can now run the server with: python manage.py runserver")

if __name__ == "__main__":
    setup_database()
