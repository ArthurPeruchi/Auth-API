from app.repositories.user_repository import UserRepository
from app.schemas.auth_schema import LoginRequest, TokenResponse
from app.infrastructure.security.password_hasher import PasswordHasher
from app.infrastructure.security.jwt import create_access_token

class InvalidCredentialsError(Exception):
    pass

class AuthUseCase:

    def __init__ (self, repository: UserRepository, password_hasher: PasswordHasher):
        self.repository = repository
        self.password_hasher = password_hasher

    def login (self, data: LoginRequest) -> TokenResponse:
        user = self.repository.get_by_email(data.email)

        if not user:
            raise InvalidCredentialsError("[!] E-mail ou senha inválidos, tente novamente.")
        
        if not self.password_hasher.verify(data.password, user.password_hash):
            raise InvalidCredentialsError("[!] E-mail ou senha inválidos, tente novamente.")

        token = create_access_token(user.id)

        return TokenResponse(access_token=token, token_type="bearer")