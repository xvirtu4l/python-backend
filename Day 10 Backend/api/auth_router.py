from fastapi import APIRouter, Depends, HTTPException, Request, UploadFile, File
from fastapi.security import OAuth2PasswordRequestForm

from factories.auth_factory import get_auth_usecase
from usecases.auth_usecase import AuthUseCase

from security.jwt_service import create_access_token, decode_token
from security.oauth2 import oauth2_scheme
from security.token_blacklist import blacklisted_tokens
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
    
    access_token = create_access_token(data={"id": user.id, "sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/logout")
def logout(token: str = Depends(oauth2_scheme)):
    blacklisted_tokens.add(token)
    return {"message": "Đăng xuất thành công"}

@router.get("/me", response_model=AuthResponse)
def read_me(
    token: str = Depends(oauth2_scheme), 
    auth_usecase: AuthUseCase = Depends(auth_service_dep)
):
    user = auth_usecase.get_current_user(token)
    return AuthResponse(
        email = user.email,
        username = user.username,
        is_active= user.is_active,
        created_at = user.created_at,
        updated_at = user.updated_at
    )
    
@router.post("/forgot-password")
def forgot_password(email: str, auth_usecase: AuthUseCase = Depends(auth_service_dep)):
    token = auth_usecase.forgot_password(email)
    return {
        "message": "Token reset password đã được gửi",
        "token": token
        }
    
@router.post("/reset-password")
def reset_password(token: str, new_password: str, auth_usecase: AuthUseCase = Depends(auth_service_dep)):
    user = auth_usecase.reset_password(token, new_password)
    if not user:
        raise HTTPException(status_code=400, detail="Token không hợp lệ hoặc đã hết hạn")
    return {"message": "Mật khẩu đã được đặt lại thành công"}

@router.post("/change-password")
def change_password(
    request: Request,
    current_password: str,
    new_password: str,
    token: str = Depends(oauth2_scheme),
    auth_usecase: AuthUseCase = Depends(auth_service_dep)
):
    # print("DEBUG: Authorization header =", request.headers.get("authorization"))
    user_payload = request.state.user
    # print("DEBUG: User payload from JWT =", user_payload)
    user_id = user_payload["id"]
    success = auth_usecase.change_password(user_id, current_password, new_password)
    
    if not success:
        raise HTTPException(status_code=400, detail="Mật khẩu hiện tại không đúng")
    
    return {"message": "Mật khẩu đã được thay đổi thành công"}