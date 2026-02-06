from repositories.user_repository import UserRepository
from usecases.password_hasher import PasswordHasher

class AuthUseCase:
    def __init__(self, user_usecase: UserRepository, password_hasher: PasswordHasher):
        self.user_usecase = user_usecase
        self.password_hasher = password_hasher
        
    def authenticate_user(self, username: str, password: str):
        user = self.user_usecase.get_user_by_username(username)
        if not user:
            return None
        if not self.password_hasher.verify_password(password, user.password):
            return None
        return user