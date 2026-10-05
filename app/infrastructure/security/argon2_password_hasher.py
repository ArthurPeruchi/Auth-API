from argon2 import PasswordHasher as Argon2Hasher
from argon2.exceptions import VerifyMismatchError, VerificationError
from .password_hasher import PasswordHasher

class Argon2PasswordHasher(PasswordHasher):
    def __init__ (self):
        self.hasher = Argon2Hasher()

    def hash (self, password: str) -> str:
        return self.hasher.hash(password)

    def verify (self, password: str, hashed_password: str) -> bool:
        try:
            return self.hasher.verify(hashed_password, password)
        except (VerifyMismatchError, VerificationError):
            return False