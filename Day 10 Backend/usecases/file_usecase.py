import uuid
from datetime import timedelta
from domain.exceptions import BusinessError

ALLOWED_TYPES = {
    "image/png",
    "image/jpeg",
    "image/jpg",
    "image/webp"
}

class FileUsecase:
    def __init__(self, minio_client, bucket:str):
        self.minio = minio_client
        self.bucket = bucket
        
    def generate_file_name(self, content_type: str):
        
        if content_type not in ALLOWED_TYPES:
            raise BusinessError("Loại file không được hỗ trợ")
        
        file_id = str(uuid.uuid4())
        object_name = file_id
        
        url = self.minio.presigned_put_object(
            bucket_name = self.bucket,
            object_name = object_name,
            expires=timedelta(minutes=15),
        )
        
        return {
            "file_id": file_id,
            "object_name": object_name,
            "upload_url": url
        }
        
    def generate_download_url(self, file_id: str):
        download_url = self.minio.presigned_get_object(
            bucket_name=self.bucket,
            object_name=file_id,
            expires=timedelta(minutes=15),
        )

        return {
            "file_id": file_id,
            "download_url": download_url
        }