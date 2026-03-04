from minio import Minio
from config.settings import get_settings

#Cái này là minio_client

settings = get_settings()

minio_client = Minio(
    endpoint="localhost:9000",
    access_key=settings.minio.access_key,
    secret_key=settings.minio.secret_key,
    secure=False
)	