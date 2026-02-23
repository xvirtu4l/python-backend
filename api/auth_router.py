from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from factories.auth_factory import get_auth_usecase
from usecases.auth_usecase import AuthUseCase

from security.jwt_service import create_access_token, decode_token
from security.oauth2 import oauth2_scheme
from schemas.auth_schema import AuthResponse

router = APIRouter(prefix="/api/auth", tags=["auth"])

def auth_service_dep() -> AuthUseCase:
    return get_auth_usecase()

@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    auth_usecase: AuthUseCase = Depends(auth_service_dep)
):
    user = auth_usecase.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Tên người dùng hoặc mật khẩu không hợp lệ")
    
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=AuthResponse)
def read_me(
    token: str = Depends(oauth2_scheme), 
    auth_usecase: AuthUseCase = Depends(auth_service_dep)
):
    user = auth_usecase.get_current_user(token)
    return AuthResponse(
        email = user.email,
        username = user.username
    )