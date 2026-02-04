from fastapi import APIRouter, Depends, HTTPException
from usecases.user_usecase import UserUseCase
from schemas.user_schema import UserResponse, UserRequest
from factories.user_factory import get_user_usecase
from domain.exceptions import BusinessError


router = APIRouter(prefix="/users", tags=["users"])
@router.post("/create", response_model=UserResponse, status_code=201)
def create(req: UserRequest, usecase: UserUseCase = Depends(get_user_usecase)):
    try:
        user = usecase.create_user(req.email, req.username, req.password)
        return UserResponse(email=user.email, username=user.username)
    except BusinessError as e:
        raise HTTPException(status_code=409, detail=str(e))

@router.get("/", response_model=list[UserResponse])
def get_users(usecase: UserUseCase = Depends(get_user_usecase)):
    users = usecase.get_users()
    return [
        UserResponse(email=user.email, username=user.username) for user in users
    ]
    