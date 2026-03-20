import uuid
from domain.entities.user import User
from domain.exceptions import BusinessError
from repositories.user_repository import UserRepository
from usecases.password_hasher import PasswordHasher

ALLOWED_TYPES = {
    "image/png",
    "image/jpeg",
    "image/jpg",
    "image/webp"
}

class UserUseCase:
    def __init__(self, repo: UserRepository, password_hasher: PasswordHasher, minio_client = None, bucket:str = None):
        self.repo = repo
        self.password_hasher = password_hasher
        self.minio = minio_client
        self.bucket = bucket

    def get_users(self):
        return self.repo.get_all_users()
    
    def create_user(self, email: str, username: str, password: str): 
        if password.lower() == email.lower() or password.lower() == username.lower():
            raise BusinessError("Mật khẩu không được trùng email hoặc tên người dùng")       
        
        hashed_password = self.password_hasher.hash_password(password)
        user = User(
            id=None,
            email=email,
            username=username,
            password=hashed_password,
            is_active=True,
            created_at= None,
            updated_at= None
            )
        self.repo.add_user(user)
        user = self.repo.get_user_by_email(email)
        return user
    
    def set_reset_password_token(self, email: str, token: str, expired_at):
        self.repo.set_reset_password_token(email, token, expired_at)
    
    def get_user_by_email(self, email: str):
        return self.repo.get_user_by_email(email)
    
    def get_user_by_username(self, username: str):
        return self.repo.get_user_by_username(username)
    
    def get_user_by_id(self, user_id: int):
        return self.repo.get_user_by_id(user_id)
    
    def get_user_by_reset_token(self, token: str):
        return self.repo.get_user_by_reset_token(token)
    
    def update_password(self, user_id: int, new_password: str):
        hashed = self.password_hasher.hash_password(new_password)
        self.repo.update_password(user_id, hashed)
    
    def clear_reset_token(self, user_id: int):
        return self.repo.clear_reset_token(user_id)
    
    # def update_avatar(self, user_id: int, object_name: str):
    #     user = self.repo.get_user_by_id(user_id)
        
    #     if not user:
    #         raise BusinessError("Người dùng không tồn tại")
        
    #     old_avatar = user.avatar_url
        
    #     if old_avatar:
    #         try:
    #             self.minio.remove_object(
    #             bucket_name=self.bucket,
    #             object_name=old_avatar
    #         )
    #         except Exception as e:
    #             print(f"Avatar not found in MinIO: {e}")
    #             pass
        
    #     self.repo.update_avatar(user_id, object_name)
        
    
    def upload_avatar(self, user_id: int, file) -> str:
        """Upload avatar file lên MinIO và cập nhật DB"""
        
        # Validate content type
        if file.content_type not in ALLOWED_TYPES:
            raise BusinessError(f"Loại file '{file.content_type}' không được hỗ trợ")
        
        # Validate file size (max 8MB)
        file.file.seek(0, 2)  # Seek to end
        file_size = file.file.tell()
        file.file.seek(0)     # Reset to start
        
        if file_size > 8 * 1024 * 1024:  # 8MB
            raise BusinessError("File quá lớn. Tối đa 8MB")
        
        # Lấy user
        user = self.repo.get_user_by_id(user_id)
        if not user:
            raise BusinessError("Người dùng không tồn tại")
        
        # Xóa avatar cũ nếu có
        old_avatar = user.avatar_url
        if old_avatar:
            try:
                self.minio.remove_object(
                    bucket_name=self.bucket,
                    object_name=old_avatar
                )
            except Exception as e:
                print(f"Old avatar not found: {e}")
        
        # Tạo tên file mới với extension
        file_id = str(uuid.uuid4())
        extension = file.filename.rsplit(".", 1)[-1] if "." in file.filename else "png"
        object_name = f"{file_id}.{extension}"
        
        # Upload lên MinIO
        try:
            self.minio.put_object(
                bucket_name=self.bucket,
                object_name=object_name,
                data=file.file,
                length=file_size,
                content_type=file.content_type
            )
        except Exception as e:
            raise BusinessError(f"Lỗi upload file: {str(e)}")
        
        # Cập nhật DB
        self.repo.update_avatar(user_id, object_name)
        
        return object_name