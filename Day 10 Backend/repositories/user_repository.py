from abc import ABC, abstractmethod

class UserRepository:
    @abstractmethod
    def exists_by_email(self, email: str) -> bool:
        """Kiểm tra xem email đã tồn tại trong hệ thống chưa."""
        pass
    
    @abstractmethod
    def exists_by_username(self, username: str) -> bool:
        """Kiểm tra xem tên người dùng đã tồn tại trong hệ thống chưa."""
        pass
    
    @abstractmethod
    def add_user(self, user):
        """Thêm một người dùng mới vào hệ thống."""
        pass
    
    @abstractmethod
    def get_all_users(self):
        """Lấy tất cả người dùng trong hệ thống."""
        pass
    
    @abstractmethod
    def get_user_by_username(self, username: str):
        """Lấy thông tin người dùng dựa trên tên người dùng."""
        pass
    
    @abstractmethod
    def get_user_by_email(self, email: str):
        """Lấy thông tin người dùng dựa trên email."""
        pass
    
    @abstractmethod
    def set_reset_password_token(self, email: str, token: str, expired_at):
        """Lưu token đặt lại mật khẩu cho người dùng dựa trên email."""
        pass
    
    @abstractmethod
    def get_user_by_reset_token(self, token: str):
        """Lấy thông tin người dùng dựa trên token đặt lại mật khẩu."""
        pass
    
    @abstractmethod
    def update_password(self, user_id: int, hashed_password: str):
        """Cập nhật mật khẩu mới cho người dùng."""
        pass
    
    @abstractmethod
    def clear_reset_token(self, user_id: int):
        """Xóa token đặt lại mật khẩu sau khi đã sử dụng."""
        pass
    
    @abstractmethod
    def get_user_by_id(self, user_id: int):
        """Lấy thông tin người dùng dựa trên ID."""
        pass
    
    