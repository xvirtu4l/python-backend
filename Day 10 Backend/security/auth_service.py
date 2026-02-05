from repositories.user_repository_mysql import UserRepositoryMySQL
from security.password_hasher import verify_password

class AuthService:
    def __init__(self, user_usecase: UserRepositoryMySQL):
        self.user_usecase = user_usecase
        
    def authenticate_user(self, username: str, password: str):
        user = self.user_usecase.get_user_by_username(username)
        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        return user