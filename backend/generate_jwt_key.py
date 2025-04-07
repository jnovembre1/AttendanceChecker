#!/usr/bin/env python3
"""
JWT Secret Key Generator

This script generates a secure random key for JWT token encoding/decoding,
encodes it in URL-safe base64 format, and provides instructions for setting
it as an environment variable in different environments.
"""

import secrets
import base64
import os
import platform

def generate_secret_key(length=32):
    """Generate a secure random key with the specified byte length."""
    return secrets.token_bytes(length)

def encode_base64_urlsafe(key_bytes):
    """Encode bytes to URL-safe base64 format."""
    return base64.urlsafe_b64encode(key_bytes).decode('utf-8')

def print_instructions(secret_key):
    """Print instructions for setting the key as an environment variable."""
    print("\n=== JWT SECRET KEY GENERATED SUCCESSFULLY ===")
    print(f"\nYour new JWT secret key is:\n{secret_key}\n")
    print("WARNING: Keep this key secure and don't share it!")
    print("This key will be used to sign and verify JWT tokens.\n")
    
    print("=== HOW TO SET AS ENVIRONMENT VARIABLE ===\n")
    
    # Check if running on Windows
    is_windows = platform.system().lower() == 'windows'
    
    print("Temporary (current session only):")
    if is_windows:
        print(f"    $env:SECRET_KEY = \"{secret_key}\"")
    else:
        print(f"    export SECRET_KEY=\"{secret_key}\"")
    
    print("\nPermanent:")
    if is_windows:
        print("    1. System level (PowerShell, run as Administrator):")
        print(f"       [Environment]::SetEnvironmentVariable('SECRET_KEY', '{secret_key}', 'Machine')")
        print("\n    2. User level (PowerShell):")
        print(f"       [Environment]::SetEnvironmentVariable('SECRET_KEY', '{secret_key}', 'User')")
        print("\n    3. Add to .env file:")
        print(f"       SECRET_KEY={secret_key}")
    else:
        print("    1. Add to ~/.profile or ~/.bashrc (for bash users):")
        print(f"       export SECRET_KEY=\"{secret_key}\"")
        print("\n    2. Add to .env file:")
        print(f"       SECRET_KEY={secret_key}")
    
    print("\nFor FastAPI/Python applications:")
    print("1. Make sure to install python-dotenv:")
    print("   pip install python-dotenv")
    print("\n2. In your main.py, update to load environment variables:")
    print("   from dotenv import load_dotenv")
    print("   load_dotenv()")
    print("   SECRET_KEY = os.getenv(\"SECRET_KEY\", \"fallback-key-for-dev-not-for-production\")")

def main():
    """Main function to generate and display the secret key."""
    key_bytes = generate_secret_key(32)  # 32 bytes = 256 bits
    secret_key = encode_base64_urlsafe(key_bytes)
    print_instructions(secret_key)

if __name__ == "__main__":
    main()

