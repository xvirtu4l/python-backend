from factories.user_factory import get_user_usecase
from usecases.auth_usecase import AuthUseCase
from security.password_hasher_interface import PasswordHasherImpl
from security.jwt_service import create_access_token, decode_token

def get_auth_usecase() -> AuthUseCase:
    user_usecase = get_user_usecase()
    password_hasher = PasswordHasherImpl()
    create_token = create_access_token
    return AuthUseCase(user_usecase, password_hasher, create_token,  decode_token = decode_token)