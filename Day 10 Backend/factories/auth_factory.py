from factories.user_factory import get_user_usecase
from usecases.auth_usecase import AuthUseCase
from security.password_hasher_interface import PasswordHasherImpl

def get_auth_usecase() -> AuthUseCase:
    user_usecase = get_user_usecase()
    password_hasher = PasswordHasherImpl()
    return AuthUseCase(user_usecase, password_hasher)