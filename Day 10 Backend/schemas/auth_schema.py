from pydantic import BaseModel

class AuthResponse(BaseModel):
    username: str
    email: str