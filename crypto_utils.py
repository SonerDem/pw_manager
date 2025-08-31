import base64
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet


# Generiert einen AES-Schlüssel aus Master-Passwort und Salt.
def generate_key(master_password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=390_000,
        backend=default_backend(),
    )
    return base64.urlsafe_b64encode(kdf.derive(master_password.encode("utf-8")))

# Erzeugt ein zufälliges Salt.
def generate_salt(length: int = 16) -> bytes:
    return os.urandom(length)

# Verschlüsselt einen Text.
def encrypt_text(text: str, fernet: Fernet) -> str:
    return fernet.encrypt(text.encode("utf-8")).decode("utf-8")

# Entschlüsselt einen Text.
def decrypt_text(token: str, fernet: Fernet) -> str:
    return fernet.decrypt(token.encode("utf-8")).decode("utf-8")
