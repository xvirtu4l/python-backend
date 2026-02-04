from config.settings import get_settings
from repositories.user_repository_mysql import UserRepositoryMySQL
from repositories.user_repository_fake import FakeUserRepository
from usecases.user_usecase import UserUseCase

def get_user_usecase():
    settings = get_settings()
    if settings.db_type == "mysql":
        repo = UserRepositoryMySQL(settings.database)
    else:
        repo = FakeUserRepository()
    return UserUseCase(repo)