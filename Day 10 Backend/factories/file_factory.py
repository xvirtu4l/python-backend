from storage.minio_conn import minio_client
from usecases.file_usecase import FileUsecase

def get_file_usecase():
    return FileUsecase(
        minio_client = minio_client,
        bucket="avatars")