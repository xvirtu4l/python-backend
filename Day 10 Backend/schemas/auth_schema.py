from pydantic import BaseModel
from datetime import datetime

class AuthResponse(BaseModel):
    username: str
    email: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    avatar_url: str | None = None
    
    class Config:
        from_attributes = True