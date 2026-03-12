from abc import ABC, abstractmethod
from typing import List, Dict

class LLMRepository(ABC):
    @abstractmethod
    async def generate_response(self, messages: List[Dict], **kwargs) -> str:
        pass
    
