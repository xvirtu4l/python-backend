from typing import Dict
import uuid
from datetime import timedelta
from domain.exceptions import BusinessError

ALLOWED_TYPES = {
    "image/png",
    "image/jpeg",
    "image/jpg",
    "image/webp"
}

CONTENT_TYPE_EXTENSIONS = {
    "image/png": ".png",
    "image/jpeg": ".jpg",
    "image/jpg": ".jpg",
    "image/webp": ".webp"
}

class FileUsecase:
    def __init__(self, minio_client, bucket:str):
        self.minio = minio_client
        self.bucket = bucket
        
    def generate_file_name(self, content_type: str) -> Dict:
        
        if content_type not in ALLOWED_TYPES:
            raise BusinessError("Loại file không được hỗ trợ")
        
        file_id = str(uuid.uuid4())
        extension = CONTENT_TYPE_EXTENSIONS.get(content_type, "")
        object_name = f"{file_id}{extension}"
        
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
        
    def generate_download_url(self, file_id: str, extension: str = "") -> Dict:
        """Generate presigned URL for file download"""
        # Validate file_id là UUID hợp lệ
        try:
            uuid.UUID(file_id)
        except ValueError:
            raise BusinessError("file_id không hợp lệ")
        
        # Reconstruct object_name với extension
        object_name = f"{file_id}{extension}" if extension else file_id
        
        try:
            download_url = self.minio.presigned_get_object(
                bucket_name=self.bucket,
                object_name=object_name,
                expires=timedelta(minutes=15),
            )
        except Exception as e:
            raise BusinessError(f"Lỗi khi tạo download URL: {str(e)}")

        return {
            "file_id": file_id,
            "download_url": download_url
        }