from abc import ABC, abstractmethod

class UserRepository:
    @abstractmethod
    def exists_by_email(self, email: str) -> bool:
        pass
    
    @abstractmethod
    def exists_by_username(self, username: str) -> bool:
        pass
    
    @abstractmethod
    def add_user(self, user):
        pass
    
    @abstractmethod
    def get_all_users(self):
        pass
    
    @abstractmethod
    def get_user_by_username(self, username: str):
        pass
    
    @abstractmethod
    def get_user_by_email(self, email: str):
        pass
    
    @abstractmethod
    def set_reset_password_token(self, email: str, token: str, expired_at):
        pass
    
    @abstractmethod
    def get_user_by_reset_token(self, token: str):
        pass
    
    @abstractmethod
    def update_password(self, user_id: int, hashed_password: str):
        pass
    
    @abstractmethod
    def clear_reset_token(self, user_id: int):
        pass
    
    @abstractmethod
    def get_user_by_id(self, user_id: int):
        pass
    
    