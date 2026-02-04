from repositories.user_repository import UserRepository
from domain.entities.user import User

class FakeUserRepository(UserRepository):
    def __init__(self):
        self.users = []

    def exists_by_email(self, email: str) -> bool:
        return any(user.email == email for user in self.users)

    def exists_by_username(self, username: str) -> bool:
        return any(user.username == username for user in self.users)

    def add_user(self, user: User):
        self.users.append(user)
    
    def get_all_users(self):
        return self.users