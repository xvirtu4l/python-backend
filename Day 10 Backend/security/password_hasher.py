from pwdlib import PasswordHash
from pwdlib.hashers import argon2

pwd_hasher = PasswordHash(hashers=[argon2.Argon2Hasher()])

def hash_password(plain_password: str) -> str:
    encoded = pwd_hasher.hash(plain_password)
    return str(encoded)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        pwd_hasher.verify(plain_password, hashed_password)
        return True
    except Exception:
        return False