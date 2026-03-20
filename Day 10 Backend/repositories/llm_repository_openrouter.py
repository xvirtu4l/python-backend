import httpx
from typing import Any, List, Dict
from repositories.llm_repository import LLMRepository
from config.settings import LLMConfig

class OpenRouterLLMRepository(LLMRepository):
    def __init__(self, config: LLMConfig):
        self.config = config
        self.client = httpx.AsyncClient(base_url=self.config.base_url, headers={
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": self.config.http_referer,
            "X-Title": self.config.x_title
        },
        timeout=60.0
        )
        
    async def generate_response(self, messages: List[Dict], **kwargs: Any) -> str:
        payload = {
            "model": self.config.model,
            "messages": messages,
            **kwargs
        }
        
        try:
            response = await self.client.post("/chat/completions", json=payload)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
        except httpx.HTTPError as e:
            print(f"Error generating LLM response: {e}")
            raise Exception("Failed to generate response from LLM") from e

    async def close(self):
        await self.client.aclose()
