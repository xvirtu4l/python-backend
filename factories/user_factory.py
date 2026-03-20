from config.settings import get_settings
from repositories.user_repository_mysql import UserRepositoryMySQL
from repositories.user_repository_fake import FakeUserRepository
from repositories.user_repository_postgres import UserRepositoryPostgres
from usecases.user_usecase import UserUseCase
from security.password_hasher_interface import PasswordHasherImpl
from storage.minio_conn import minio_client

def get_user_usecase():
    settings = get_settings()
    if settings.db_type == "mysql":
        repo = UserRepositoryMySQL(settings.database)

    elif settings.db_type == "postgres":
        repo = UserRepositoryPostgres()

    elif settings.db_type == "fake":
        repo = FakeUserRepository()

    else:
        raise ValueError(f"Unsupported DB_TYPE: {settings.db_type}")
    password_hasher = PasswordHasherImpl()
    return UserUseCase(repo, password_hasher, minio_client=minio_client, bucket="avatars")