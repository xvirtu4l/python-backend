from pydantic import BaseModel, EmailStr, Field
from typing_extensions import Annotated

class UserRequest(BaseModel):
    email: EmailStr
    username: Annotated[str, Field(min_length=3, max_length=50)]
    password: Annotated[str, Field(min_length=8)]
    
class UserResponse(BaseModel):
    email: EmailStr
    username: str
    
    class Config:
        from_attributes = True