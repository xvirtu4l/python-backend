from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from factories.auth_factory import get_auth_usecase
from usecases.auth_usecase import AuthUseCase

from security.jwt_service import create_access_token, decode_token
from security.oauth2 import oauth2_scheme

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
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me")
def read_me(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    return {"username": payload.get("sub")}