import secrets

secret_key = secrets.token_urlsafe(32)  # Generates a 32-character random key
print(secret_key)