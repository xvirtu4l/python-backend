from abc import ABC, abstractmethod
from typing import List, Dict

class LLMRepository(ABC):
    @abstractmethod
    async def generate_response(self, messages: List[Dict], **kwargs) -> str:
        """Gọi API của mô hình ngôn ngữ lớn để tạo phản hồi dựa trên danh sách tin nhắn đã cho."""
        pass
