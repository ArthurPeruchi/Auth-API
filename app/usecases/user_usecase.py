from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserCreate, UserUpdate, UserPatch
from app.infrastructure.security.password_hasher import PasswordHasher

class UserNotFoundError(Exception):
    pass

class EmailAlreadyExistsError(Exception):
    pass

class UserUseCase:

    def __init__ (self, repository: UserRepository, password_hasher: PasswordHasher):
        self.repository = repository
        self.password_hasher = password_hasher

    def create (self, data: UserCreate) -> User:
        existing_user = self.repository.get_by_email(data.email)

        if existing_user:
            raise EmailAlreadyExistsError("[!] Email já cadastrado.")

        user = User(name=data.name, email=data.email, password_hash=self.password_hasher.hash(data.password))

        return self.repository.create(user)

    def get_by_id (self, user_id: int) -> User:
        user = self.repository.get_by_id(user_id)

        if not user:
            raise UserNotFoundError("[!] Usuário não encontrado.")

        return user

    def get_by_email (self, user_email: str) -> User:
        user = self.repository.get_by_email(user_email)

        if not user:
            raise UserNotFoundError("[!] Usuário não encontrado.")

        return user

    def update (self, user_id: int, data: UserUpdate) -> User:
        user = self.repository.get_by_id(user_id)

        if not user:
            raise UserNotFoundError("[!] Usuário não encontrado.")

        existing_user = self.repository.get_by_email(data.email)
        
        if existing_user and existing_user.id != user_id:
            raise EmailAlreadyExistsError("[!] Email já cadastrado.")

        user.name = data.name
        user.email = data.email

        if data.password:
            user.password_hash = self.password_hasher.hash(data.password)

        return self.repository.update(user)

    def patch (self, user_id: int, data: UserPatch) -> User:
        user = self.repository.get_by_id(user_id)

        if not user:
            raise UserNotFoundError("[!] Usuário não encontrado.")

        if data.email is not None:
            existing_user = self.repository.get_by_email(data.email)
            
            if existing_user and existing_user.id != user_id:
                raise EmailAlreadyExistsError("[!] Email já cadastrado.")
            user.email = data.email

        if data.name is not None:
            user.name = data.name

        if data.password is not None:
            user.password_hash = self.password_hasher.hash(data.password)

        return self.repository.update(user)