from abc import ABC, abstractmethod

class ConversationRepository(ABC):
    @abstractmethod
    def create_conversation(self, user_id: int, title: str):
        pass
    
    @abstractmethod
    def get_conversations_by_user_id(self, user_id: int):
        pass
    
    @abstractmethod
    def get_conversation_by_user_id(self, user_id: int):
        pass
    
    @abstractmethod
    def get_conversation_by_id(self, conversation_id: int):
        pass
    
    @abstractmethod
    def delete_conversation(self, conversation_id: int):
        pass