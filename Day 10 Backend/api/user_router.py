from fastapi import APIRouter, Depends, HTTPException, Request, UploadFile, File
from usecases.user_usecase import UserUseCase
from schemas.user_schema import UserResponse, UserRequest
from factories.user_factory import get_user_usecase
from domain.exceptions import BusinessError

from security.oauth2 import oauth2_scheme
from security.jwt_service import get_current_user


router = APIRouter(prefix="/users", tags=["users"])
@router.post("/create", response_model=UserResponse, status_code=201)
def create(req: UserRequest, usecase: UserUseCase = Depends(get_user_usecase)):
    try:
        user = usecase.create_user(req.email, req.username, req.password)
        return UserResponse(
            email = user.email,
            username = user.username,
            is_active= user.is_active,
            created_at = user.created_at,
            updated_at = user.updated_at,
            avatar_url = user.avatar_url
        )
    except BusinessError as e:
        raise HTTPException(status_code=409, detail=str(e))

@router.get("/", response_model=list[UserResponse])
def get_users(usecase: UserUseCase = Depends(get_user_usecase), token: str = Depends(oauth2_scheme)):
    users = usecase.get_users()
    return [
        UserResponse(email=user.email, username=user.username, is_active=user.is_active, created_at=user.created_at, updated_at=user.updated_at, avatar_url=user.avatar_url) for user in users
    ]

@router.get("/me")
def me(request: Request, token: str = Depends(oauth2_scheme)):
    user = request.state.user
    
    return {
        "user": user,
        "token": token
    }

@router.put("/avatar")
# def update_avatar(
#     object_name: str,
#     current_user: dict = Depends(get_current_user),
#     usecase: UserUseCase = Depends(get_user_usecase)
# ):
#     print(current_user)
#     try:
#         usecase.update_avatar(current_user["id"], object_name)
#         return {"message": "Cập nhật avatar thành công"}
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))
    
def update_avatar(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
    usecase: UserUseCase = Depends(get_user_usecase)
):
    try:
        object_name = usecase.upload_avatar(current_user["id"], file)
        return {
            "message": "Cập nhật avatar thành công",
            "object_name": object_name
        }
    except BusinessError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))