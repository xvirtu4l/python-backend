from abc import ABC, abstractmethod

class ConversationRepository(ABC):
    @abstractmethod
    def create_conversation(self, user_id: int, title: str):
        """Tạo một cuộc trò chuyện mới cho người dùng với tiêu đề đã cho."""
        pass
    
    @abstractmethod
    def get_conversations_by_user_id(self, user_id: int):
        """Lấy tất cả các cuộc trò chuyện của một người dùng."""
        pass
    
    @abstractmethod
    def get_conversation_by_user_id(self, user_id: int):
        """Lấy cuộc trò chuyện gần nhất của một người dùng."""
        pass
    
    @abstractmethod
    def get_conversation_by_id(self, conversation_id: int):
        """Lấy thông tin của một cuộc trò chuyện dựa trên ID."""
        pass
    
    @abstractmethod
    def delete_conversation(self, conversation_id: int):
        """Xóa một cuộc trò chuyện dựa trên ID."""
        pass