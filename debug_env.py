#!/usr/bin/env python3
"""Debug environment variable loading"""

import os
from dotenv import load_dotenv

print("=== Environment Debug ===")
print(f"Current working directory: {os.getcwd()}")

# Load .env file explicitly
env_path = os.path.join(os.getcwd(), '.env')
print(f"Looking for .env at: {env_path}")
print(f".env file exists: {os.path.exists(env_path)}")

if os.path.exists(env_path):
    with open(env_path, 'r') as f:
        content = f.read()
        print("\n.env file content:")
        print(content)

load_dotenv()

print("\nEnvironment variables after loading .env:")
for key in ['LOG_LEVEL', 'LOG_FORMAT', 'LOG_FILE', 'PORT', 'FLASK_DEBUG']:
    value = os.getenv(key)
    print(f"  {key} = {value}")

print("\nAll environment variables with 'LOG' in name:")
for key, value in os.environ.items():
    if 'LOG' in key.upper():
        print(f"  {key} = {value}")