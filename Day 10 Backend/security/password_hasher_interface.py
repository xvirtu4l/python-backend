from pwdlib import PasswordHash
from pwdlib.hashers import argon2

from usecases.password_hasher import PasswordHasher

class PasswordHasherImpl(PasswordHasher):

    def __init__(self):
        self.pwd_hasher = PasswordHash(hashers=[argon2.Argon2Hasher()])

    def hash_password(self, plain_password: str) -> str:
        encoded = self.pwd_hasher.hash(plain_password)
        return str(encoded)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        try:
            self.pwd_hasher.verify(plain_password, hashed_password)
            return True
        except Exception:
            return False