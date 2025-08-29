# security.py
import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv

# Load the environment variables from .env file
load_dotenv()

# Load the encryption key from environment variable
key = os.getenv("ENCRYPTION_KEY").encode()
cipher_suite = Fernet(key)

def encrypt_data(data: str) -> bytes:
    """Encrypts a string."""
    return cipher_suite.encrypt(data.encode())

def decrypt_data(encrypted_data: bytes) -> str:
    """Decrypts a string."""
    return cipher_suite.decrypt(encrypted_data).decode()