from pydantic import BaseModel, Field
from typing import List, Optional

# ========== Request Schemas ==========

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=4000)
    conversation_id: Optional[int] = None

# ========== Response Schemas ==========

class ChatResponse(BaseModel):
    conversation_id: int
    user_message: dict
    assistant_message: dict

class MessageResponse(BaseModel):
    id: int
    role: str
    content: str
    created_at: Optional[str] = None

class ConversationResponse(BaseModel):
    id: int
    title: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

class ConversationDetailResponse(BaseModel):
    conversation: ConversationResponse
    messages: List[MessageResponse]