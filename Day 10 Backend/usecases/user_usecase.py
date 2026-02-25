from domain.entities.user import User
from domain.exceptions import BusinessError
from usecases.password_hasher import PasswordHasher

class UserUseCase:
    def __init__(self, repo, password_hasher: PasswordHasher):
        self.repo = repo
        self.password_hasher = password_hasher
        
    def get_users(self):
        return self.repo.get_all_users()
    
    def create_user(self, email: str, username: str, password: str): 
        if password.lower() == email.lower() or password.lower() == username.lower():
            raise BusinessError("Mật khẩu không được trùng email hoặc tên người dùng")       
        
        hashed_password = self.password_hasher.hash_password(password)
        user = User(
            id=None,
            email=email,
            username=username,
            password=hashed_password,
            is_active=True
            )
        self.repo.add_user(user)
        return user
    
    def set_reset_password_token(self, email: str, token: str, expired_at):
        self.repo.set_reset_password_token(email, token, expired_at)
    
    def get_user_by_email(self, email: str):
        return self.repo.get_user_by_email(email)
    
    def get_user_by_username(self, username: str):
        return self.repo.get_user_by_username(username)
    
    def get_user_by_id(self, user_id: int):
        return self.repo.get_user_by_id(user_id)
    
    def get_user_by_reset_token(self, token: str):
        return self.repo.get_user_by_reset_token(token)
    
    def update_password(self, user_id: int, new_password: str):
        hashed = self.password_hasher.hash_password(new_password)
        self.repo.update_password(user_id, hashed)
    
    def clear_reset_token(self, user_id: int):
        return self.repo.clear_reset_token(user_id)
    