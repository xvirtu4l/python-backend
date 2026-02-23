from repositories.user_repository import UserRepository
from usecases.password_hasher import PasswordHasher
from domain.exceptions import BusinessError

class AuthUseCase:
    def __init__(self, user_usecase: UserRepository, password_hasher: PasswordHasher, create_token, decode_token):
        self.user_usecase = user_usecase
        self.password_hasher = password_hasher
        self.create_token = create_token
        self.decode_token = decode_token

    def authenticate_user(self, username: str, password: str):
        user = self.user_usecase.get_user_by_username(username)
        if not user:
            return None
        if not self.password_hasher.verify_password(password, user.password):
            return None
        return user
    
    def login(self, username: str, password: str) -> str:
        user = self.authenticate_user(username, password)
        if not user:
            return None
        
        token = self.create_token({"sub": user.username})
        return token    
    
    def get_current_user(self, token: str):
        payload = self.decode_token(token)
        
        username = payload.get("sub")
        
        if not username:
            raise BusinessError("Invalid Token Payload")
        
        user = self.user_usecase.get_user_by_username(username)
        if not user:
            raise BusinessError("User not Found")
        
        return user