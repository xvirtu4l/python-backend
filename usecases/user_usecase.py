from domain.entities.user import User
from domain.exceptions import BusinessError

class UserUseCase:
    def __init__(self, repo):
        self.repo = repo
        
    def get_users(self):
        return self.repo.get_all_users()
    
    def create_user(self, email: str, username: str, password: str): 
        if password.lower() == email.lower() or password.lower() == username.lower():
            raise BusinessError("Mật khẩu không được trùng email hoặc tên người dùng")       
        user = User(email, username, password)
        self.repo.add_user(user)
        return user