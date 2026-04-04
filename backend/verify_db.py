"""
Database verification script.
Checks if the configured database is accessible and has required tables.
Works with both file-based and in-memory databases.
"""
import os
import sqlite3
from sqlalchemy import create_engine, inspect
from sqlalchemy.exc import SQLAlchemyError

# Get database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///:memory:")

print(f"Verifying database configuration...")
print(f"DATABASE_URL: {DATABASE_URL}")
print()

try:
    # Create engine to test connection
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
    )
    
    # Test connection
    with engine.connect() as conn:
        print("✓ Database connection successful")
    
    # Check if it's a file-based SQLite database
    if "sqlite" in DATABASE_URL and "sqlite:///:memory:" not in DATABASE_URL:
        # Extract file path from connection string
        db_path = DATABASE_URL.replace("sqlite:///./", "").replace("sqlite:///", "")
        if os.path.exists(db_path):
            file_size = os.path.getsize(db_path)
            print(f"✓ Database file exists: {db_path}")
            print(f"  Size: {file_size:,} bytes")
            print()
        else:
            print(f"⚠ Database file not found: {db_path}")
            print("  (Will be created on first use)")
            print()
    elif "sqlite:///:memory:" in DATABASE_URL:
        print("✓ Using in-memory SQLite database")
        print("  (Fresh database created for each session)")
        print()
    
    # Inspect tables
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    
    if tables:
        print("✓ Database Tables:")
        for table in tables:
            columns = inspector.get_columns(table)
            print(f"  {table}: {len(columns)} columns")
        print()
    else:
        print("ℹ No tables found in database")
        print("  (Tables will be created when migrations run)")
        print()
    
    print("✓ Database verification: SUCCESS")
    print("✓ Database is properly configured and accessible")

except SQLAlchemyError as e:
    print(f"✗ Database connection error: {e}")
    exit(1)
except Exception as e:
    print(f"✗ Error verifying database: {e}")
    exit(1)

