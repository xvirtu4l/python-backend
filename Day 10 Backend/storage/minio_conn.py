from minio import Minio
from config.settings import get_settings

#Cái này là minio_client

settings = get_settings()

minio_client = Minio(
    endpoint=settings.minio.endpoint,
    access_key=settings.minio.access_key,
    secret_key=settings.minio.secret_key,
    secure=False
)	
