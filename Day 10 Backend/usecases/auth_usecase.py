import uuid
from repositories.user_repository import UserRepository
from usecases.password_hasher import PasswordHasher
from domain.exceptions import BusinessError
from datetime import datetime, timedelta, timezone

class AuthUseCase:
    def __init__(self, user_usecase: UserRepository, password_hasher: PasswordHasher, create_token, decode_token):
        self.user_usecase = user_usecase
        self.password_hasher = password_hasher
        self.create_token = create_token
        self.decode_token = decode_token

    def authenticate_user(self, username: str, password: str):
        credential = username.strip()
        user = self.user_usecase.get_user_by_username(credential)
        if not user and "@" in credential:
            user = self.user_usecase.get_user_by_email(credential)
        if not user:
            return None
        if not self.password_hasher.verify_password(password, user.password):
            return None
        return user
    
    def login(self, username: str, password: str) -> str:
        user = self.authenticate_user(username, password)
        if not user:
            return None
        
        token = self.create_token({"id": user.id, "sub": user.username})
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
    
    def forgot_password(self, email: str):
        user = self.user_usecase.get_user_by_email(email)
        if not user:
            raise BusinessError("User not Found")
        
        token = str(uuid.uuid4())
        expired_at = datetime.now(timezone.utc) + timedelta(minutes=15)
        self.user_usecase.set_reset_password_token(email, token, expired_at)
        return token
    
    def reset_password(self, token: str, new_password: str):
        user = self.user_usecase.get_user_by_reset_token(token)
        if not user:
            raise BusinessError("Token không hợp lệ hoặc đã hết hạn")
        self.user_usecase.update_password(user.id, new_password)
        self.user_usecase.clear_reset_token(user.id)
        return user
    
    def change_password(self, user_id: int, old_password: str, new_password: str):
        user = self.user_usecase.get_user_by_id(user_id)
        if not user:
            raise BusinessError("User not Found")
        if not self.password_hasher.verify_password(old_password, user.password):
            raise BusinessError("Mật khẩu cũ không đúng")
        self.user_usecase.update_password(user.id, new_password)
        return True
