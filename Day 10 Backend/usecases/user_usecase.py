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
    
    def get_user_by_username(self, username: str):
        return self.repo.get_user_by_username(username)