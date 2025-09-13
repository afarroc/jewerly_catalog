#!/usr/bin/env python
"""
Script to test S3 configuration and connectivity
Run this script to debug S3 upload issues in production
"""
import os
import sys
import django
from pathlib import Path

# Setup Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jewerly_catalog.settings_production')
django.setup()

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from jewerly_catalog.settings_production import (
    AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY,
    AWS_STORAGE_BUCKET_NAME, AWS_S3_REGION_NAME
)

def test_s3_configuration():
    """Test S3 configuration and connectivity"""
    print("=== S3 Configuration Test ===\n")

    # Check environment variables
    print("1. Environment Variables:")
    print(f"   AWS_ACCESS_KEY_ID: {'✓ Set' if AWS_ACCESS_KEY_ID else '✗ Not set'}")
    print(f"   AWS_SECRET_ACCESS_KEY: {'✓ Set' if AWS_SECRET_ACCESS_KEY else '✗ Not set'}")
    print(f"   AWS_STORAGE_BUCKET_NAME: {AWS_STORAGE_BUCKET_NAME or '✗ Not set'}")
    print(f"   AWS_S3_REGION_NAME: {AWS_S3_REGION_NAME or 'us-east-2 (default)'}")
    print()

    # Check storage configuration
    print("2. Storage Configuration:")
    print(f"   Default storage: {default_storage.__class__.__name__}")
    print(f"   Storage location: {getattr(default_storage, 'location', 'N/A')}")
    print(f"   Bucket name: {getattr(default_storage, 'bucket_name', 'N/A')}")
    print()

    # Test basic connectivity
    print("3. Connectivity Test:")
    try:
        # Try to list bucket contents (limited to 1 item)
        objects = list(default_storage.bucket.objects.limit(1))
        print(f"   ✓ Can connect to bucket")
        print(f"   ✓ Found {len(objects)} test objects")
        if objects:
            print(f"   ✓ Sample object: {objects[0].key}")
    except Exception as e:
        print(f"   ✗ Cannot connect to bucket: {str(e)}")
    print()

    # Test file upload
    print("4. Upload Test:")
    test_content = b"Hello, S3! This is a test file."
    test_filename = "test_s3_upload.txt"

    try:
        # Save test file
        file_obj = ContentFile(test_content)
        saved_name = default_storage.save(test_filename, file_obj)
        print(f"   ✓ File uploaded successfully: {saved_name}")

        # Check if file exists
        exists = default_storage.exists(saved_name)
        print(f"   ✓ File exists in storage: {exists}")

        # Get file URL
        file_url = default_storage.url(saved_name)
        print(f"   ✓ File URL: {file_url}")

        # Clean up - delete test file
        default_storage.delete(saved_name)
        print(f"   ✓ Test file cleaned up")

    except Exception as e:
        print(f"   ✗ Upload test failed: {str(e)}")
        print(f"   ✗ Exception type: {type(e).__name__}")
    print()

    print("=== Test Complete ===")

if __name__ == "__main__":
    test_s3_configuration()