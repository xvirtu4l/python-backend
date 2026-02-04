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