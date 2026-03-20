from pydantic import BaseModel, EmailStr, Field
from typing_extensions import Annotated
from datetime import datetime

class UserRequest(BaseModel):
    email: EmailStr
    username: Annotated[str, Field(min_length=3, max_length=50)]
    password: Annotated[str, Field(min_length=8, max_length=128)]
    
class UserResponse(BaseModel):
    email: EmailStr
    username: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    avatar_url: str | None = None
    
    class Config:
        from_attributes = True