from abc import ABC, abstractmethod

class MessageRepository(ABC):
    @abstractmethod
    def add_message(self, message):
        """Thêm một tin nhắn mới vào cuộc trò chuyện."""
        pass
    
    @abstractmethod
    def get_messages_by_conversation_id(self, conversation_id: int):
        """Lấy tất cả tin nhắn trong một cuộc trò chuyện."""
        pass
