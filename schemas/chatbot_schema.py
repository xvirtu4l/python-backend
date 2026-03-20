from pydantic import BaseModel, Field
from datetime import datetime
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
    created_at: datetime

class ConversationResponse(BaseModel):
    id: int
    title: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class ConversationDetailResponse(BaseModel):
    conversation: ConversationResponse
    messages: List[MessageResponse]