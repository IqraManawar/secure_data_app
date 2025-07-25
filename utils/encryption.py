import hashlib
from cryptography.fernet import Fernet

# Encryption Key (for demo, should be stored securely in production)
KEY = Fernet.generate_key()
cipher = Fernet(KEY)

def hash_passkey(passkey):
    return hashlib.sha256(passkey.encode()).hexdigest()

def encrypt_data(text):
    return cipher.encrypt(text.encode()).decode()

def decrypt_data(encrypted_text, hashed_passkey, stored_data):
    for record in stored_data.values():
        if record["encrypted_text"] == encrypted_text and record["passkey"] == hashed_passkey:
            return cipher.decrypt(encrypted_text.encode()).decode()
    return None
