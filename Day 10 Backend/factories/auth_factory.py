from factories.user_factory import get_user_usecase
from security.auth_service import AuthService

def get_auth_service() -> AuthService:
    user_usecase = get_user_usecase()
    return AuthService(user_usecase)